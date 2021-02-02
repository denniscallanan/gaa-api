
from peewee import *
from pydantic import BaseModel

from src.api.clients.base import BaseClient, BaseDataModel
from src.api.exceptions import generic_error_wrapper
from src.api.models.response_models import ResponseModel


class Championship(BaseDataModel):
    championship_id = AutoField()
    championship_name = CharField()
    descript = CharField(null=True)

    class Meta:
        table_name = 'championship'


class ChampionshipResponse(BaseModel):
    championship_id: int
    championship_name: str
    descript: str


class ChampionshipResponseModel(ResponseModel):
    result: ChampionshipResponse


class ChampionshipClient(BaseClient):

    def db_model_to_response(self, db_model) -> ChampionshipResponse:
        return ChampionshipResponse(**self._get_field_args(db_model))

    @generic_error_wrapper
    def get_championship(self, championship_id):
        championship = Championship.get_by_id(championship_id)
        response = self.db_model_to_response(championship)
        return self.to_response_model(response)
