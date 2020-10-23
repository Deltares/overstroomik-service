from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PORT: int = 8000
    GEOSERVER_URL: str = "http://geoserver:8080/geoserver"
    GEOSERVER_LAYER: str = "overstroomik:Overstroomik_data"

    LAYER_EVACUATION_PERCENTAGE: str  = "evacuatie_evacuatiefractie_verwachtingswaarde"
    LAYER_SAFETY_BOARD_ID: str  = "administratieve_grenzen_veiligheidsregios"
    LAYER_FLOOD_TYPE: str  = "gebiedsindeling_floodtype"
    LAYER_MAXIMUM_WATER_DEPTH: str  = "overstroomik_opvullen_combined_waterdiepte"
    LAYER_PROBABILITY_OF_FLOODING: str  = "plaatsgebonden_kans_totaal_2019_0"
    
    FIELD_EVACUATION_PERCENTAGE: str  = "VERWACHTIN"
    FIELD_SAFETY_BOARD_ID: str  = "id"
    FIELD_FLOOD_TYPE: str  = "status"
    FIELD_MAXIMUM_WATER_DEPTH: str  = "GRAY_INDEX"
    FIELD_PROBABILITY_OF_FLOODING: str  = "KLASSE@"    

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
