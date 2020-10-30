"""
This class uses the geoserver-api and geoserver layers to find
location information by rd coordinates
"""

from typing import Optional
import httpx
import sys
from overstroomik_service.auto_models import Data, ProbabilityOfFlooding
from overstroomik_service.errors import Errors
from overstroomik_service.config import settings


class Geoserver():

    @staticmethod
    async def get_data(rd_x: float,
                       rd_y: float,
                       geoserver_url: str = settings.GEOSERVER_URL,
                       layers: str = settings.GEOSERVER_LAYER):
        """
        Find location information with specified rd coordinates.
        :param rd_x: x coordinate in meters, geocoded location longitude transformed into EPSG:28992
        :param rd_y: y coordinate in meters, geocoded location latitude transformed into EPSG:28992
        :param geoserver_url: link to the geoserver (example: http://geoserver:8080/geoserver)
        :param layers: group layer with the expected data  (example: overstroomik:Overstroomik_data)
        """

        # initial no error
        status = Errors.ERROR_GENERAL_NOER

        # start with empty object
        data = Data()

        # create the getfeature info url
        url, params, coordinate_is_valid, indices = Geoserver.get_api_url_from_rd(
            rd_x=rd_x, rd_y=rd_y, geoserver_url=geoserver_url)

        # Check input, is location between the layer exent
        if not coordinate_is_valid:
            status = Errors.ERROR_GEOS_NO_SMAP
        else:
            # connect async to the geoserver
            async with httpx.AsyncClient() as client:

                # fetch the feature info
                try:
                    result = await client.get(url=url, params=params, timeout=settings.FETCH_TIMEOUT)
                    if result.status_code == httpx.codes.OK:
                        out = result.json()
                        features = out.get("features")
                        status, data = Geoserver.to_data(features)
                    else:
                        status = Errors.ERROR_GEOS_NO_RESP

                except:
                    status = Errors.ERROR_GEOS_NO_RESP

        return status, data

    @staticmethod
    def to_data(features: dict):

        # start with empty object
        data = Data()

        # initial no error
        status = Errors.ERROR_GENERAL_NOER
        
        if len(features) > 0:

            data_item = {}

            for data_layer in settings.data_layers:
                property = data_layer["property"]
                layer = data_layer["layer"]
                field = data_layer["field"]

                data_item[property] = Geoserver.get_item(
                    features=features, layer=layer, field=field)

            data = Data(**data_item)
        else:
            status: Errors.ERROR_GEOS_NO_SMAP

        return status, data

    @staticmethod
    def get_item(features: dict, layer: str, field: str):

        value = None

        for feature in features:
            f_id = feature.get("id")
            properties = feature.get("properties")
            
            # the raster layer has no id in de json data (features),
            # so we have one layer with an empty string. When we need
            # more raster layers, the field (GRAY_INDEX) must
            # used and must be unique
            if layer == "" and f_id == "":
                value = properties.get(field, None)
                            
            elif len(layer) > 0 and f_id.startswith(layer):               
                value = properties.get(field, None)                

        return value

    @staticmethod
    def get_api_url_from_rd(rd_x: float,
                            rd_y: float,
                            geoserver_url: Optional[str] = settings.GEOSERVER_URL,
                            layers: [str] = settings.GEOSERVER_LAYER):
        """
        Create the get-feature-info link.
        :param rd_x: x coordinate in meters, geocoded location longitude transformed into EPSG:28992
        :param rd_y: y coordinate in meters, geocoded location latitude transformed into EPSG:28992
        :param geoserver_url: link to the geoserver (example: http://geoserver:8080/geoserver)
        :param layers: group layer with the expected data  (example: overstroomik:Overstroomik_data)

        The 'getfeatureinfo' of the geoserver requires a bbox+width+height+x+y,
        so we have to calculate the correct indices by ourselves, which is why
        this can be hardcoded. The x and y are integer coordinates in pixels
        """

        # api url template
        url = f"{geoserver_url}/overstroomik/wms"

        # bounding box (extent of the group layer)
        min_x = settings.grouplayer_extent_rd["min_x"]
        min_y = settings.grouplayer_extent_rd["min_y"]
        max_x = settings.grouplayer_extent_rd["max_x"]
        max_y = settings.grouplayer_extent_rd["max_y"]

        # test the input coordinate is in layer-extend
        coordinate_is_valid = rd_x >= min_x and rd_x <= max_x and rd_y >= min_y and rd_y <= max_y

        # calculate the height and width
        height = max_y - min_y
        width = max_x - min_x

        # calculate x/y relative to the extent
        ddx = rd_x - min_x
        ddy = rd_y - min_y

        # calculate then x/y in pixels
        x = width * ddx / width
        y = height - (height * ddy / height)

        # bounding box format
        bounding_box = f"{min_x},{min_y},{max_x},{max_y}"

        indices = (width, height, x, y)

        params = {
            "SERVICE": "WMS",
            "VERSION": "1.1.1",
            "REQUEST": "GetFeatureInfo",
            "INFO_FORMAT": "application/json",
            "SRS": "EPSG:28992",
            "FEATURE_COUNT": "50",
            "LAYERS": layers,
            "QUERY_LAYERS": layers,
            "BBOX": bounding_box,
            "WIDTH": int(width),
            "HEIGHT": int(height),
            "X": int(x),
            "Y": int(y)
        }

        return url, params, coordinate_is_valid, indices
