
from peewee import *
from playhouse.shortcuts import model_to_dict

from src.api.base import BaseModel
from src.api.exceptions import generic_error_wrapper


class Team(BaseModel):
    team_id = AutoField(unique=True, primary_key=True)
    team_name = CharField()
    sport = CharField()
    est_year = IntegerField()
    is_county = BooleanField()


class TeamClient:

    @generic_error_wrapper
    def get_team(self, team_id):
        team = Team.get(Team.team_id == team_id)
        return model_to_dict(team)
