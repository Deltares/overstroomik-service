from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PORT: int = 8000
    PDOK_API = "https://geodata.nationaalgeoregister.nl/locatieserver/v3/free"
    WS_VERSION = 0.1

    ERROR_GENERAL_NOER = "no-error"
    ERROR_PDOK_NO_RESP = "Geen response PDOK"
    ERROR_PDOK_NO_RESU = "Geen eenduidige resultaat PDOK"
    ERROR_GEOS_NO_RESP = "Geen response geoserver"
    ERROR_GEOS_NO_SMAP = "Geen response specifieke kaart"
    ERROR_GENERAL_ERRO = "Service niet bereikbaar"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
