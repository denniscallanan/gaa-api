from peewee import *
from pydantic import BaseModel

from src.api.clients.base import BaseDataModel, BaseClient
from src.api.exceptions import generic_error_wrapper
from src.api.models.response_models import ResponseModel


class PortalUser(BaseDataModel):
    user_identifier = AutoField(null=True)
    google_sub = CharField(null=True)
    reported_count = IntegerField(default=0)

    class Meta:
        table_name = 'portal_user'


class PortalUserResponse(BaseModel):
    user_identifier: int
    google_sub: str
    reported_count: int


class PortalUserResponseModel(ResponseModel):
    result: PortalUserResponse


class PortalUserClient(BaseClient):

    def db_model_to_response(self, db_model) -> PortalUserResponse:
        return PortalUserResponse(**self._get_field_args(db_model))

    @generic_error_wrapper
    def get_user(self, user_identifier):
        user = PortalUser.get_by_id(user_identifier)
        response = self.db_model_to_response(user)
        return self.to_response_model(response)

    @generic_error_wrapper
    def create_or_get_user_by_google_sub(self, google_sub_id):
        user = PortalUser.get_or_none(PortalUser.google_sub == google_sub_id)
        if not user:
            user = PortalUser(google_sub=google_sub_id)
            user.save()
        response = self.db_model_to_response(user)
        return self.to_response_model(response)
