from pydantic import BaseModel, Field, ConfigDict, StrictInt, field_validator
from pydantic_geojson import (
    FeatureCollectionModel, FeatureModel, PointModel,
    PolygonModel, MultiPointModel, MultiPolygonModel)
from uuid import UUID
from typing import Annotated, Optional, Literal, Union, List
from datetime import date, timedelta

MODEL_CONFIG = ConfigDict(extra='forbid')

TODAY_DATE = date.today()
YESTERDAY_DATE = date.today() - timedelta(days=1)


# yesterday = lambda: date.today() - timedelta(days=1)
def yesterday() -> date:
    return date.today() - timedelta(days=1)


# Administrative Service Section
class DistrictInfo(BaseModel):
    model_config = MODEL_CONFIG

    district_code: Optional[Annotated[StrictInt, Field(
        ge=100, le=999,
        description="District code (3 digits)",
        example=523)]] = None
    is_pocra: Optional[Annotated[Literal[0, 1],	Field(
        description="0 for non-project districts, 1 for project districts, omit for all",
        example=1)]] = None
    phase: Optional[Annotated[Literal[0, 1, 2],	Field(
        description=(
            "0 for non-project districts,",
            "1 for project districts of phase-I,",
            "2 for project districts of phase-II and omit for all-phases"),
        example=1)]] = None


class TalukaInfo(BaseModel):
    model_config = MODEL_CONFIG

    district_code: Optional[Annotated[StrictInt, Field(
        ge=100, le=999, description="District code (3 digits)", example=523)]] = None
    taluka_code: Optional[Annotated[StrictInt, Field(
        ge=1000, le=9999, description="Taluka code (4 digits)", example=4224)]] = None
    is_pocra: Optional[Annotated[Literal[0, 1], Field(
        description="0 for non-project districts, 1 for project districts, omit for all", example=1)]] = None
    phase: Optional[Annotated[Literal[0, 1, 2], Field(
        description=(
            "0 for non-project talukas,",
            "1 for project talukas of phase-I,",
            "2 for project talukas of phase-II and omit for all-phases"),
        example=2)]] = None


class VillageInfo(BaseModel):
    model_config = MODEL_CONFIG

    district_code: Optional[
        Annotated[StrictInt, Field(ge=100, le=999, description="District code (3 digits)", example=516)]
        ] = None
    taluka_code: Optional[
        Annotated[StrictInt, Field(ge=1000, le=9999, description="Taluka code (4 digits)", example=4153)]
        ] = None
    village_code: Optional[
        Annotated[StrictInt, Field(ge=100000, le=999999, description="Village code (6 digits)", example=551117)]
        ] = None
    is_pocra: Optional[
        Annotated[
            Literal[0, 1],
            Field(
                description="0 for non-project districts, 1 for project districts, omit for all",
                example=1)]
        ] = None
    phase: Optional[
        Annotated[
            Literal[0, 1, 2],
            Field(
                description=(
                    "0 for non-project villages,"
                    "1 for project villages of phase-I,"
                    "2 for project villages of phase-II and omit for all-phases"
                ),
                example=2)]] = None


class LocationRequest(BaseModel):
    model_config = MODEL_CONFIG

    longitude: float = Field(..., description="Longitude of the location", example=74.51)
    latitude: float = Field(..., description="Latitude of the location", example=19.51)


class DatatableRequest(BaseModel):
    draw: int = Field(default=1, description="Page number to draw", example=1)
    start: int = Field(default=0, gte=0, description="Page number of datatable start", example=0)
    length: int = Field(default=10, ge=1, le=100, description="Lenght of table rows", example=10)
    search_value: str = Field(
        default="Nashik",
        alias="search[value]",
        max_length=300,
        description="DataTables search value",
        example='Nashik')


# Weather Service Section
class WeatherRainYear(BaseModel):
    model_config = MODEL_CONFIG

    rain_year: StrictInt = Field(..., description="rain year to fetch data", example=2024)


class WeatherInfo(BaseModel):
    model_config = MODEL_CONFIG

    longitude: float = Field(..., description="Longitude of the location", example=74.51)
    latitude: float = Field(..., description="Latitude of the location", example=19.51)
    start_date: Optional[date] = Field(
        None,
        description="Start date for which weather data is required",
        example="2025-06-20")
    end_date: Optional[date] = Field(
        None,
        description="End date for which weather data is required",
        example="2025-06-20")


class WeatherBlockInfo(BaseModel):
    model_config = MODEL_CONFIG

    block_id: StrictInt = Field(..., description="Forecast block ID", example=4751)
    for_date: date = Field(
        default_factory=date.today,
        description="date for which weather forecast data is required",
        example=TODAY_DATE
        )


class WeatherStationInfo(BaseModel):
    model_config = MODEL_CONFIG

    station_id: Optional[int] = Field(
        default=None,
        description="Skymet weather station ID",
        example=152
    )
    for_date: Optional[date] = Field(
        default_factory=yesterday,
        description="date for which weather data is required",
        example=YESTERDAY_DATE
    )


class WeatherStationHourlyInfo(BaseModel):
    model_config = MODEL_CONFIG

    station_id: StrictInt = Field(..., description="Skymet weather station ID", example=152)
    for_date: date = Field(
        ..., default_factory=yesterday, description="date for which weather data is required", example=YESTERDAY_DATE
        )


class WeatherQueryRange(BaseModel):
    model_config = MODEL_CONFIG

    station_id: StrictInt = Field(..., description="Skymet weather station ID", example=152)
    for_date: date = Field(
        default_factory=date.today, description="date for which weather data is required", example=TODAY_DATE
        )
    for_period: Annotated[
        Literal['last_day', 'last_week', 'last_month', 'till_day'],
        Field(default="last_day", description="period for which weather data is required", example="last_day")
        ]


class WeatherDate(BaseModel):
    model_config = MODEL_CONFIG

    for_date: date = Field(
        default_factory=date.today, description="date for which weather data is required", example=YESTERDAY_DATE
        )


class DistrictWeatherInfo(BaseModel):
    model_config = MODEL_CONFIG

    district_code: Optional[
        Annotated[StrictInt, Field(ge=100, le=999, description="District code (3 digits)", example=523)]
        ] = None


class TalukaWeatherInfo(BaseModel):
    model_config = MODEL_CONFIG

    district_code: Optional[
        Annotated[StrictInt, Field(ge=100, le=999, description="District code (3 digits)", example=523)]
        ] = None
    taluka_code: Optional[
        Annotated[StrictInt, Field(ge=1000, le=9999, description="Taluka code (4 digits)", example=4224)]
        ] = None


class TalukaDateWeatherInfo(BaseModel):
    model_config = MODEL_CONFIG

    district_code: Optional[
        Annotated[StrictInt, Field(ge=100, le=999, description="District code (3 digits)", example=523)]
        ] = None
    taluka_code: Optional[
        Annotated[StrictInt, Field(ge=1000, le=9999, description="Taluka code (4 digits)", example=4224)]
        ] = None
    for_date: date = Field(
        default_factory=date.today, description="date for which weather data is required", example=YESTERDAY_DATE
        )


class VillageWeatherInfo(BaseModel):
    model_config = MODEL_CONFIG

    district_code: Optional[
        Annotated[StrictInt, Field(ge=100, le=999, description="District code (3 digits)", example=523)]
        ] = None
    taluka_code: Optional[
        Annotated[StrictInt, Field(ge=1000, le=9999, description="Taluka code (4 digits)", example=4215)]
        ] = None
    village_code: Optional[
        Annotated[StrictInt, Field(ge=100000, le=999999, description="Village code (6 digits)", example=558733)]
        ] = None


# Farmer Application Service Section
class SoilInfo(BaseModel):
    model_config = MODEL_CONFIG

    village_code: Annotated[
        StrictInt, Field(ge=100000, le=999999, description="Village code (6 digits)", example=559481)
        ]
    survey_number: StrictInt = Field(..., description="Survey number to fetch data", example=457)


class Soilhealth(BaseModel):
    model_config = MODEL_CONFIG

    shc_no: str = Field(..., description="Soil Health Card number (10 digits)", example='MH559481/2018-19/123022361/7')


# Waterbalance Section
class WbPointDeficitInfo(BaseModel):
    model_config = MODEL_CONFIG

    for_date: date = Field(
        default_factory=date.today, description="date for which weather data is required", example=YESTERDAY_DATE
        )

    district_code: Optional[
        Annotated[StrictInt, Field(ge=100, le=999, description="District code (3 digits)", example=523)]
        ] = None
    taluka_code: Optional[
        Annotated[StrictInt, Field(ge=1000, le=9999, description="Taluka code (4 digits)", example=4224)]
        ] = None
    village_code: Optional[
        Annotated[StrictInt, Field(ge=100000, le=999999, description="Village code (6 digits)", example=551117)]
        ] = None

    major_crop: Optional[
        Annotated[StrictInt, Field(ge=100000, le=999999, description="Village code (6 digits)", example=551117)]
        ] = None
    soil_profile: Optional[
        Annotated[StrictInt, Field(ge=100000, le=999999, description="Village code (6 digits)", example=551117)]
        ] = None
    delta_days: Optional[
        Annotated[StrictInt, Field(ge=100000, le=999999, description="Village code (6 digits)", example=551117)]
        ] = None


# DBT section
class DbtApplicationsInfo(BaseModel):
    model_config = MODEL_CONFIG

    application_id: Optional[
        Annotated[StrictInt, Field(ge=3000000, le=1000000000, description="Application id (7 digits)", example=3000046)]
        ] = None
    desk: Optional[Annotated[Literal[2, 4],	Field(description="dbt phase", example=2)]] = None


# MLP App Section
class SurveyNumber(BaseModel):
    gat_no: Optional[list[str]] = None
    sub_gat_no: Optional[list[str]] = None


class MlpProperties(BaseModel):
    model_config = MODEL_CONFIG

    act_id: int
    structure_type: str = "unknown"
    survey_number: Optional[SurveyNumber] = None
    area: Optional[float] = None
    note: Optional[str] = ""
    user_id: int
    vincode: int
    monsoon_year: Optional[int] = None
    no_of_structures: int = Field(default=1, ge=0)

    @field_validator("no_of_structures", mode="before")
    @classmethod
    def normalize_no_of_structures(cls, v):
        return 1 if v is None or v <= 0 else v


class PatchedPoint(PointModel):
    bbox: Optional[List[float]] = None


class PatchedPolygon(PolygonModel):
    bbox: Optional[List[float]] = None


class PatchedMultiPoint(MultiPointModel):
    bbox: Optional[List[float]] = None


class PatchedMultiPolygon(MultiPolygonModel):
    box: Optional[List[float]] = None


GeometryType = Annotated[
    Union[PatchedPoint, PatchedPolygon, PatchedMultiPoint, PatchedMultiPolygon], Field(discriminator="type")
    ]


class MlpFeature(FeatureModel):
    geometry: GeometryType
    properties: MlpProperties


EXAMPLE_FEATURE_COLLECTION = {
        "type": "FeatureCollection",
        "features": [
                {
                        "type": "Feature",
                        "properties": {
                                "act_id": 313,
                                "structure_type": "Proposed",
                                "survey_number": {
                                        "gat_no": ["20"],
                                        "sub_gat_no": ["21-2"]
                                },
                                "area": 0.0,
                                "note": "test",
                                "user_id": 42000554,
                                "vincode": 558736,
                                "monsoon_year": 2024,
                                "no_of_structures": 5
                        },
                        "geometry": {
                                "type": "Point",
                                "coordinates": [
                                        74.91629612889022,
                                        19.179641335461667
                                ]
                        }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "act_id": 343,
                        "structure_type": "Proposed",
                        "survey_number": {
                            "gat_no": [
                                "20-25",
                                "12 to 25",
                                "20",
                                "24",
                                "25"
                            ],
                            "sub_gat_no": [
                                "21-2"
                            ]
                        },
                        "area": 10,
                        "note": "test",
                        "user_id": 42000554,
                        "vincode": 558736,
                        "monsoon_year": 2024,
                        "no_of_structures": 10
                    },
                    "geometry": {
                        "coordinates": [
                            [
                                [
                                    75.21292693972725,
                                    19.2678181097518
                                ],
                                [
                                    75.21292693972725,
                                    19.070652053784883
                                ],
                                [
                                    75.31180389285237,
                                    19.070652053784883
                                ],
                                [
                                    75.31180389285237,
                                    19.2678181097518
                                ],
                                [
                                    75.21292693972725,
                                    19.2678181097518
                                ]
                            ]
                        ],
                        "type": "Polygon"
                    }
                }
        ]
}


class MlpFeatureCollection(FeatureCollectionModel):
    features: list[MlpFeature]
    model_config = {"json_schema_extra": {"example": EXAMPLE_FEATURE_COLLECTION}}


class GeomType(BaseModel):
    model_config = MODEL_CONFIG
    geom_type: Literal["Point", "Polygon"] = Field(
        description="Geometry type can either be point or a polygon", example="Point"
        )


class StructureGeoJsonInfo(BaseModel):
    model_config = MODEL_CONFIG

    village_code: Optional[
        Annotated[StrictInt, Field(ge=100000, le=999999, description="Village code (6 digits)", example=541256)]
        ] = None
    monsoon_year: StrictInt = Field(2024, description="4 digit monsoon year to fetch data", example=2024)


class ExistingStructureInfo(BaseModel):
    model_config = MODEL_CONFIG

    id: Annotated[StrictInt, Field(ge=1, description="dbt other existing activity id", example=1)]


class ProposedStructureInfo(BaseModel):
    model_config = MODEL_CONFIG

    id: Annotated[
        UUID, Field(description="dbt other existing activity UUID", example="b846d546-2670-4495-8e69-85af661902b2")
        ]


class NrmApplicationInfo(ProposedStructureInfo):
    model_config = MODEL_CONFIG

    note: Annotated[str, Field(description="Note for deletion", example="Testing API")]
    del_by: Annotated[str, Field(description="Deleted by (user_id)", example="4225_Anjanpur_SDO")]
    del_roleid: Annotated[int, Field(description="Role ID of the user deleting the record", example=23)]


class NrmApplicationStatusInfo(ProposedStructureInfo):
    model_config = MODEL_CONFIG

    status: Annotated[
        Literal[0, 1, 2], Field(description="0 for pending, 1 for approved & 2 for rejected", example=1)
        ]
    apr_rej_by: Annotated[
        str, Field(description="Application approved or rejected by (user_id)", example="4225_Anjanpur_TAO")
        ]
    apr_rej_roleid: Annotated[
        int, Field(description="Role ID of the user approving or rejecting the application", example=19)
        ]


class ProposedStructureGeoRequest(StructureGeoJsonInfo):
    model_config = MODEL_CONFIG

    act_id: Optional[
        Annotated[
            StrictInt,
            Field(ge=100, le=999, description="Activity code (3 digits)", example=308)
        ]] = None


class DataTableInfo(VillageWeatherInfo):
    model_config = MODEL_CONFIG

    draw: int = Field(default=1, description="Page number to draw", example=1)
    start: int = Field(default=0, gte=0, description="Page number of datatable start", example=0)
    length: int = Field(default=10, ge=1, le=50, description="Lenght of table rows", example=10)
