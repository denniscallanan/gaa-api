
from peewee import *
from playhouse.shortcuts import model_to_dict

from src.api.base import BaseModel
from src.api.exceptions import generic_error_wrapper


class Venue(BaseModel):
    year_built = IntegerField(null=True)
    venue_county = CharField(null=True)
    venue_id = AutoField()
    venue_name = CharField()

    class Meta:
        table_name = 'venue'


class VenueClient:

    @generic_error_wrapper
    def get_venue(self, venue_id):
        venue = Venue.get(Venue.venue_id == venue_id)
        return model_to_dict(venue)
