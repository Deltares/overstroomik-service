from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PORT: int = 8000
    FETCH_TIMEOUT: float = 10.0
    GEOSERVER_URL: str = "http://geoserver:8080/geoserver"
    GEOSERVER_LAYER: str = "overstroomik:Overstroomik_data"

    data_layers: list = [{
        "property": "maximum_water_depth",
        "layer": "",  # "overstroomik_opvullen_combined_waterdiepte",
        "field": "GRAY_INDEX"}, {
        "property": "safety_board_id",
        "layer": "administratieve_grenzen_veiligheidsregios",
        "field": "id"}, {
        "property": "probability_of_flooding",
        "layer": "plaatsgebonden_kans_totaal_2019_0",
        "field": "KLASSE@"}, {
        "property": "evacuation_percentage",
        "layer": "evacuatie_evacuatiefractie_verwachtingswaarde",
        "field": "VERWACHTIN"}, {
        "property": "flood_type",
        "layer": "gebiedsindeling_floodtype",
        "field": "status"}]

    @ validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
