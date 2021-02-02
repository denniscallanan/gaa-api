from typing import Optional

from peewee import *
from pydantic import BaseModel

from src.api.clients.base import BaseDataModel, BaseClient
from src.api.exceptions import generic_error_wrapper
from src.api.models.response_models import ResponseModel


class Venue(BaseDataModel):
    year_built = IntegerField(null=True)
    venue_county = CharField(null=True)
    venue_id = AutoField()
    venue_name = CharField()

    class Meta:
        table_name = 'venue'


class VenueResponse(BaseModel):
    year_built: Optional[int]
    venue_county: str
    venue_id: int
    venue_name: str


class VenueResponseModel(ResponseModel):
    result: VenueResponse


class VenueClient(BaseClient):

    def db_model_to_response(self, db_model) -> VenueResponse:
        return VenueResponse(**self._get_field_args(db_model))

    @generic_error_wrapper
    def get_venue(self, venue_id):
        venue = Venue.get_by_id(venue_id)
        response = self.db_model_to_response(venue)
        return self.to_response_model(response)
