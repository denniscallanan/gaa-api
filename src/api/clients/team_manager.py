from datetime import date
from typing import Optional

from peewee import *
from pydantic import BaseModel

from src.api.clients.base import BaseDataModel, BaseClient
from src.api.exceptions import generic_error_wrapper
from src.api.models.response_models import ResponseModel


class TeamManager(BaseDataModel):
    position_end = DateField(null=True)
    position_start = DateField(null=True)
    team_id = IntegerField()
    dob = DateField(null=True)
    full_name = CharField()
    team_manager_id = AutoField()

    class Meta:
        table_name = 'team_manager'


class TeamManagerResponse(BaseModel):
    position_end: Optional[date]
    position_start: Optional[date]
    team_id: int
    dob: Optional[date]
    full_name: str
    team_manager_id: int


class TeamManagerResponseModel(ResponseModel):
    result: TeamManagerResponse


class TeamManagerClient(BaseClient):

    def db_model_to_response(self, db_model) -> TeamManagerResponse:
        return TeamManagerResponse(**self._get_field_args(db_model))

    @generic_error_wrapper
    def get_team_manager(self, team_manager_id):
        team_manager = TeamManager.get_by_id(team_manager_id)
        response = self.db_model_to_response(team_manager)
        return self.to_response_model(response)
