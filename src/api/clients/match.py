from datetime import date
from typing import Optional

from peewee import *
from pydantic import BaseModel

from src.api.clients.base import BaseDataModel, BaseClient
from src.api.exceptions import generic_error_wrapper
from src.api.models.response_models import ResponseModel


class Match(BaseDataModel):
    away_team_goals = IntegerField()
    away_team_id = IntegerField()
    away_team_manager_id = IntegerField()
    home_team_manager_id = IntegerField()
    away_team_points = IntegerField()
    championship_id = IntegerField()
    championship_round = CharField(null=True)
    extra_time = BooleanField(null=True)
    full_time = BooleanField(null=True)
    half_time = BooleanField(null=True)
    home_team_goals = IntegerField()
    home_team_id = IntegerField()
    home_team_points = IntegerField()
    is_replay = BooleanField(constraints=[SQL("DEFAULT false")])
    match_date = DateField(null=True)
    match_time = TimeField(null=True)
    referee_id = IntegerField()
    match_id = AutoField()
    venue_id = IntegerField()

    class Meta:
        table_name = 'match'


class MatchResponse(BaseModel):
    away_team_goals: int
    away_team_id: int
    away_team_manager_id: Optional[int]
    home_team_manager_id: Optional[int]
    away_team_points: int
    championship_id: Optional[int]
    championship_round: Optional[str]
    extra_time: bool
    full_time: bool
    half_time: bool
    home_team_goals: int
    home_team_id: int
    home_team_points: int
    is_replay: bool
    match_date: Optional[date]
    match_time: Optional[str]
    referee_id: Optional[int]
    match_id: int


class MatchResponseModel(ResponseModel):
    result: MatchResponse


class MatchClient(BaseClient):

    def db_model_to_response(self, db_model) -> MatchResponse:
        return MatchResponse(**self._get_field_args(db_model))

    @generic_error_wrapper
    def get_match(self, match_id):
        match = Match.get_by_id(match_id)
        response = self.db_model_to_response(match)
        return self.to_response_model(response)
