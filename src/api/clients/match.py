from datetime import date
from typing import Optional

from peewee import *

from src.api.clients.base import BaseDataModel, DTO
from src.api.models.response_models import ResponseModel


class MatchTable(BaseDataModel):
    id_tag = CharField(default=BaseDataModel.gen_uid("MATCH"))
    away_team_goals = IntegerField(default=0)
    away_team_id = CharField()
    away_team_manager_id = CharField()
    home_team_manager_id = CharField()
    away_team_points = IntegerField(default=0)
    championship_id = CharField()
    championship_round = CharField(null=True)
    extra_time = BooleanField(null=True)
    full_time = BooleanField(null=True)
    half_time = BooleanField(null=True)
    home_team_goals = IntegerField(default=0)
    home_team_id = CharField()
    home_team_points = IntegerField(default=0)
    is_replay = BooleanField(constraints=[SQL("DEFAULT false")])
    match_date = DateField(null=True)
    match_time = TimeField(null=True)
    referee_id = CharField()
    venue_id = CharField()
    version_num = IntegerField(null=False, default=0)
    created_by = IntegerField(null=False, default=0)
    recorded_timestamp = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'match'
        primary_key = CompositeKey('id_tag', 'version_num')


class Match(DTO):
    away_team_goals: Optional[int]
    away_team_id: Optional[str]
    away_team_manager_id: Optional[str]
    home_team_manager_id: Optional[str]
    away_team_points: Optional[int]
    championship_id: Optional[str]
    championship_round: Optional[str]
    extra_time: Optional[bool]
    full_time: Optional[bool]
    half_time: Optional[bool]
    home_team_goals: Optional[int]
    home_team_id: Optional[str]
    home_team_points: Optional[int]
    is_replay: Optional[bool]
    match_date: Optional[date]
    match_time: Optional[str]
    referee_id: Optional[str]

    @classmethod
    def get_required_fields(cls):
        return ["home_team_id", "away_team_id", "match_date"]

    @classmethod
    def get_uneditable_fields(cls):
        return ["home_team_id", "away_team_id"]


class MatchResponseModel(ResponseModel):
    result: Match.get_identified_record()
