from enum import Enum


class Errors(Enum):
    ERROR_GENERAL_IMEP = "Invalid or missing endpoint request"
    ERROR_GENERAL_NOER = "No error"
    ERROR_GENERAL_ERRO = "Service not available"
    ERROR_OUT_OF_BOUND = "Location is out of bounds"
    ERROR_GEOS_NO_RESP = "No response geoserver"
    ERROR_GEOS_NO_SMAP = "No response geoserver map layer"
    ERROR_PDOK_NO_RESP = "No response PDOK"
    ERROR_PDOK_NO_RESU = "No valid result PDOK"
    ERROR_BY_LOCATION_422 = "No valid input for parameter or missing parameter search_field, latitude or longitude"
    ERROR_BY_RD_422 = "No valid input for parameter or missing parameter x or y"
