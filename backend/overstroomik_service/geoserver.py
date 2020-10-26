"""
This class uses the geoserver-api and geoserver layers to find
location information by rd coordinates
"""

from typing import Optional
import httpx
import sys
from overstroomik_service.auto_models import Data
from overstroomik_service.config import settings

ERROR_GENERAL_NOER = "no-error"
ERROR_GEOS_NO_RESP = "Geen response geoserver"
ERROR_GEOS_NO_SMAP = "Geen response specifieke kaart"


class Geoserver():

    async def get_data(self,
                       rd_x: float,
                       rd_y: float,
                       geoserver_url: Optional[str] = settings.GEOSERVER_URL,
                       layers: [str] = settings.GEOSERVER_LAYER):
        """
        Find location information with specified rd coordinates.
        :param rd_x: x coordinate in meters, geocoded location longitude transformed into EPSG:28992
        :param rd_y: y coordinate in meters, geocoded location latitude transformed into EPSG:28992
        :param geoserver_url: link to the geoserver (example: http://geoserver:8080/geoserver)
        :param layers: group layer with the expected data  (example: overstroomik:Overstroomik_data)
        """

        # initial no error
        status = ERROR_GENERAL_NOER

        # start with empty object
        data_item = {}

        # create the getfeature info url
        api_info = self.get_api_url_from_rd(
            rd_x=rd_x, rd_y=rd_y, geoserver_url=geoserver_url)

        url = api_info.get("api_url")

        # Check input, is location between the layer exent
        if api_info.get("valid", True) is False:
            status = ERROR_GEOS_NO_SMAP
        else:
            # connect async to the geoserver
            async with httpx.AsyncClient() as client:

                # fetch the feature info                
                try:
                    result = await client.get(url, timeout=10.0)
                                
                    if result.status_code == httpx.codes.OK:

                        out = result.json()
                        features = out.get("features")

                        if len(features) > 0:

                            for feature in features:

                                # id or name of the sub layer
                                f_id = feature.get("id")
                                properties = feature.get("properties")

                                if len(f_id) == 0 or f_id.startswith(
                                        settings.LAYER_MAXIMUM_WATER_DEPTH):
                                    data_item["maximum_water_depth"] = properties.get(
                                        settings.FIELD_MAXIMUM_WATER_DEPTH, None)

                                elif f_id.startswith(settings.LAYER_SAFETY_BOARD_ID):
                                    data_item["safety_board_id"] = properties.get(
                                        settings.FIELD_SAFETY_BOARD_ID, None)

                                elif f_id.startswith(
                                        settings.LAYER_PROBABILITY_OF_FLOODING):
                                    data_item["probability_of_flooding"] = properties.get(
                                        settings.FIELD_PROBABILITY_OF_FLOODING, None)

                                elif f_id.startswith(settings.LAYER_EVACUATION_PERCENTAGE):
                                    data_item["evacuation_percentage"] = properties.get(
                                        settings.FIELD_EVACUATION_PERCENTAGE, None)

                                elif f_id.startswith(settings.LAYER_FLOOD_TYPE):
                                    data_item["flood_type"] = properties.get(
                                        settings.FIELD_FLOOD_TYPE, None)

                            else:
                                status: ERROR_GEOS_NO_SMAP
                    else:
                        status = ERROR_GEOS_NO_RESP
                        
                except :                    
                    status = ERROR_GEOS_NO_RESP                                       

        return status, Data(**data_item)

    def get_api_url_from_rd(self,
                            rd_x: float,
                            rd_y: float,
                            geoserver_url: Optional[str] = settings.GEOSERVER_URL,
                            layers: [str] = settings.GEOSERVER_LAYER):
        """
        Create the get-feature-info link.
        :param rd_x: x coordinate in meters, geocoded location longitude transformed into EPSG:28992
        :param rd_y: y coordinate in meters, geocoded location latitude transformed into EPSG:28992
        :param geoserver_url: link to the geoserver (example: http://geoserver:8080/geoserver)
        :param layers: group layer with the expected data  (example: overstroomik:Overstroomik_data)
        """

        # api url template
        api_get_feature_info = f"{geoserver_url}/overstroomik/wms?SERVICE=WMS&VERSION=1.1.1"\
            f"&REQUEST=GetFeatureInfo&INFO_FORMAT=application/json&SRS=EPSG:28992&FEATURE_COUNT=50"\
            f"&LAYERS={layers}&QUERY_LAYERS={layers}"

        # bounding box
        bounding_box_rd = {
            "min_x": float(634),
            "min_y": float(306594),
            "max_x": float(284300),
            "max_y": float(636981)
        }

        # test the input coordinate is in layer-extend
        test_coordinate = rd_x >= bounding_box_rd.get(
            "min_x") and rd_x <= bounding_box_rd.get(
            "max_x") and rd_y >= bounding_box_rd.get(
            "min_y") and rd_y <= bounding_box_rd.get("max_y")

        # calculate the height and width
        height = bounding_box_rd.get("max_y") - bounding_box_rd.get("min_y")
        width = bounding_box_rd.get("max_x") - bounding_box_rd.get("min_x")

        # calculate x/y relative to the extent
        ddx = rd_x - bounding_box_rd.get("min_x")
        ddy = rd_y - bounding_box_rd.get("min_y")

        # calculate then x/y in pixels
        x = width * ddx / width
        y = height - (height * ddy / height)

        # bounding box format
        bounding_box = f"{bounding_box_rd['min_x']},{bounding_box_rd['min_y']}"\
            f",{bounding_box_rd['max_x']},{bounding_box_rd['max_y']}"

        return {
            "valid": test_coordinate,
            "height": height,
            "width": width,
            "x": x,
            "y": y,
            "api_url": f"{api_get_feature_info}&BBOX={bounding_box}&WIDTH={int(width)}"
            f"&HEIGHT={int(height)}&X={int(x)}&Y={int(y)}"
        }
