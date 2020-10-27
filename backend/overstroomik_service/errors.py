from enum import Enum

class Errors(Enum):
    ERROR_GENERAL_NOER = "no-error"
    ERROR_GENERAL_ERRO = "Service niet bereikbaar"
    ERROR_GENERAL_0422 = "No valid input for search_field or latitude and longitude"
    ERROR_GEOS_NO_RESP = "Geen response geoserver"
    ERROR_GEOS_NO_SMAP = "Geen response specifieke kaart"    
    ERROR_PDOK_NO_RESP = "Geen response PDOK"
    ERROR_PDOK_NO_RESU = "Geen eenduidige resultaat PDOK"        

    def __str__(self):
        return '%s' % self.value