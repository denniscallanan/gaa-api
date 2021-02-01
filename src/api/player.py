
from peewee import *
from playhouse.shortcuts import model_to_dict

from src.api.base import BaseModel
from src.api.team import Team
from src.api.exceptions import generic_error_wrapper


class Player(BaseModel):
    caps = IntegerField(null=True)
    career_end = DateField(null=True)
    career_start = DateField(null=True)
    dob = DateField(null=True)
    full_name = CharField()
    player_id = AutoField()
    team = ForeignKeyField(column_name='team_id', field='team_id', model=Team, null=True)
    typical_position = CharField(null=True)

    class Meta:
        table_name = 'player'



class PlayerClient:

    @generic_error_wrapper
    def get_player(self, player_id):
        player = Player.get(Player.player_id == player_id)
        return model_to_dict(player)
