from datetime import date
from typing import Optional

from peewee import *
from pydantic import BaseModel

from src.api.clients.base import BaseDataModel, BaseClient
from src.api.exceptions import generic_error_wrapper
from src.api.models.response_models import ResponseModel


class Referee(BaseDataModel):
    career_end = DateField(null=True)
    career_start = DateField(null=True)
    county = CharField(null=True)
    dob = DateField(null=True)
    full_name = CharField()
    referee_id = AutoField()

    class Meta:
        table_name = 'referee'


class RefereeResponse(BaseModel):
    career_end: Optional[date]
    career_start: Optional[date]
    county: str
    dob: Optional[date]
    full_name: str
    referee_id: int


class RefereeResponseModel(ResponseModel):
    result: RefereeResponse


class RefereeClient(BaseClient):

    def db_model_to_response(self, db_model) -> RefereeResponse:
        return RefereeResponse(**self._get_field_args(db_model))

    @generic_error_wrapper
    def get_referee(self, referee_id):
        referee = Referee.get_by_id(referee_id)
        response = self.db_model_to_response(referee)
        return self.to_response_model(response)
