
from peewee import *
from playhouse.shortcuts import model_to_dict

from src.api.base import BaseModel
from src.api.venue import Venue
from src.api.exceptions import generic_error_wrapper


class Team(BaseModel):
    est_year = SmallIntegerField(null=True)
    is_county = BooleanField(constraints=[SQL("DEFAULT true")])
    main_venue = ForeignKeyField(column_name='main_venue_id', field='venue_id', model=Venue, null=True)
    sport = CharField(null=True)
    team_id = AutoField()
    team_name = CharField()

    class Meta:
        table_name = 'team'


class TeamClient:

    @generic_error_wrapper
    def get_team(self, team_id):
        team = Team.get_by_id(team_id)
        return model_to_dict(team)
