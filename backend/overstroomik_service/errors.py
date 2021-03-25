from enum import Enum


class Errors(Enum):
    
    ERROR_GENERAL_NOER = {"errorcode": 0, "status": "No error"}
    ERROR_PDOK_NO_RESU = {"errorcode": 1, "status": "No valid result PDOK"}
    ERROR_PDOK_NO_RESP = {"errorcode": 2, "status": "No response PDOK"}
    ERROR_GEOS_NO_RESP = {"errorcode": 3, "status": "No response geoserver"}
    ERROR_GEOS_NO_SMAP = {"errorcode": 4, "status": "No response geoserver map layer"}        
    ERROR_GENERAL_IMEP = {"errorcode": 5, "status": "Invalid or missing endpoint request"}    
    ERROR_OUT_OF_BOUND = {"errorcode": 6, "status": "Location is out of bounds"}    
    ERROR_BY_LOCATION_422 = {"errorcode": 7, "status": "No valid input for parameter or missing parameter search_field, latitude or longitude"}
    # ERROR_GENERAL_ERRO = {"errorcode": 103, "status": "Service not available"}
    # ERROR_BY_RD_422 = {"errorcode": 104, "status": "No valid input for parameter or missing parameter x or y"}