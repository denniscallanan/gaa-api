
from peewee import *
from playhouse.shortcuts import model_to_dict

from src.api.base import BaseModel
from src.api.exceptions import generic_error_wrapper


class Referee(BaseModel):
    career_end = DateField(null=True)
    career_start = DateField(null=True)
    county = CharField(null=True)
    dob = DateField(null=True)
    full_name = CharField()
    referee_id = AutoField()

    class Meta:
        table_name = 'referee'


class RefereeClient:

    @generic_error_wrapper
    def get_referee(self, referee_id):
        referee = Referee.get_by_id(referee_id)
        return model_to_dict(referee)
