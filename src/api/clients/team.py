
from typing import Optional

from peewee import *
from pydantic import BaseModel

from src.api.clients.base import BaseDataModel, BaseClient
from src.api.exceptions import generic_error_wrapper
from src.api.models.response_models import ResponseModel


class Team(BaseDataModel):
    est_year = SmallIntegerField(null=True)
    is_county = BooleanField(constraints=[SQL("DEFAULT true")])
    main_venue_id = IntegerField()
    sport = CharField(null=True)
    team_id = AutoField()
    team_name = CharField()

    class Meta:
        table_name = 'team'


class TeamResponse(BaseModel):
    team_id: int
    team_name: str
    main_venue_id: Optional[int]
    sport: str
    is_county: bool
    estabilished_year: Optional[int]


class TeamResponseModel(ResponseModel):
    result: TeamResponse


class TeamClient(BaseClient):

    def db_model_to_response(self, db_model) -> TeamResponse:
        return TeamResponse(**self._get_field_args(db_model))

    @generic_error_wrapper
    def get_team(self, team_id):
        team = Team.get_by_id(team_id)
        response = self.db_model_to_response(team)
        return self.to_response_model(response)
