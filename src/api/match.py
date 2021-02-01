
from peewee import *
from playhouse.shortcuts import model_to_dict

from src.api.base import BaseModel
from src.api.championship import Championship
from src.api.team import Team
from src.api.referee import Referee
from src.api.venue import Venue
from src.api.exceptions import generic_error_wrapper


class Match(BaseModel):
    away_team_goals = IntegerField()
    away_team = ForeignKeyField(column_name='away_team_id', field='team_id', model=Team)
    away_team_points = IntegerField()
    championship = ForeignKeyField(
        column_name='championship_id', field='championship_id', model=Championship, null=True)
    championship_round = CharField(null=True)
    extra_time = BooleanField(null=True)
    full_time = BooleanField(null=True)
    half_time = BooleanField(null=True)
    home_team_goals = IntegerField()
    home_team = ForeignKeyField(backref='team_home_team_set', column_name='home_team_id', field='team_id', model=Team)
    home_team_points = IntegerField()
    is_replay = BooleanField(constraints=[SQL("DEFAULT false")])
    match_date = DateField(null=True)
    match_time = TimeField(null=True)
    referee = ForeignKeyField(column_name='referee_id', field='referee_id', model=Referee, null=True)
    match_id = AutoField()
    venue = ForeignKeyField(column_name='venue_id', field='venue_id', model=Venue, null=True)

    class Meta:
        table_name = 'match'


class MatchClient:

    @generic_error_wrapper
    def get_match(self, match_id):
        match = Match.get_by_id(match_id)
        return model_to_dict(match)
