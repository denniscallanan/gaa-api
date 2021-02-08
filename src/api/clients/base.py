import random 
import string

from typing import Optional, Type
from fastapi import HTTPException

from peewee import *
from playhouse.db_url import connect
from pydantic import BaseModel

from src.helpers import get_field_args
from src.api.models.response_models import ResponseModel
from src.constants import ServerConfig


db = connect(ServerConfig.DATABASE_URL, autorollback=True)


class Fields:
    VERSION_NUM = 'version_num'
    CREATED_BY = 'created_by'
    ID_TAG = 'id_tag'


class DTO(BaseModel):

    def to_table(self, table_class):
        return table_class(**get_field_args(self, nested_structure=False))

    @classmethod
    def get_required_fields(cls):
        return []

    @classmethod
    def get_uneditable_fields(cls):
        return []

    @classmethod
    def get_uneditable_class_fields(cls):
        return []


    @classmethod
    def get_identified_record(cls):
        class Entry(cls):
            id_tag: Optional[str]
        Entry.__name__ = cls.__name__ + "Entry"
        return Entry

    @classmethod
    def get_editable_model(cls):
        class Entry(cls):
            pass
        for field in cls.get_uneditable_class_fields():
            try:
                del field
            except Exception:
                print(f"Could not delete: {field}")
        Entry.__name__ = "Editable" + cls.__name__
        return Entry

class BaseDataModel(Model):
    class Meta:
        database = db

    def to_model(self, model_type):
        return model_type(**get_field_args(self))

    def to_response_model(self, model_type, success=True):
        status = "success" if success else "failure"
        return ResponseModel(status=status, result=self.to_model(model_type))

    @staticmethod
    def gen_uid(prefix):
        return prefix + '_' + (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12)))


class BaseClient:

    ### PUBLIC

    def to_response_model(self, item: ResponseModel, success=True):
        status = "success" if success else "failure"
        return ResponseModel(status=status, result=item)

    def merge(self, existing, incoming):
        existing = self._sanitize_table_dict(dict(existing))
        incoming = self._sanitize_table_dict(dict(incoming))
        existing.update(incoming)
        return existing


    ### PUBLIC API-LAYER

    def get_by_id(self, id_tag, table_class) -> BaseDataModel:
        return table_class.select().where(table_class.id_tag == id_tag).order_by(table_class.version_num.desc()).first()

    def insert(self, obj, table_class, user):
        if not all(self._field_existence(obj, obj.get_required_fields())):
            raise HTTPException(
                status_code=400, 
                detail=f"Must supply the following fields: {obj.get_required_fields()}"
            )
        if getattr(obj, Fields.ID_TAG, None) is not None:
            raise HTTPException(
                status_code=400,
                detail="Cannot supply id_tag when inserting new record"
            )
        table_dict = self._sanitize_table_dict(dict(obj))
        table_dict[Fields.CREATED_BY] = user.id_tag
        return table_class.create(**table_dict)

    def update(self, id_tag, obj, table_class: Type[BaseDataModel], user):
        if any(self._field_existence(obj, obj.get_uneditable_fields())):
            raise HTTPException(
                status_code=400,
                detail=f"The following fields cannot be updated: {obj.get_uneditable_fields()}"    
            )
        model_class = type(obj)
        most_recent_record = self.get_by_id(id_tag, table_class)
        most_recent_version = most_recent_record.version_num

        most_recent_record_model = most_recent_record.to_model(model_class)
        
        new_record_dict = self.merge(most_recent_record_model, obj)
        new_record_dict[Fields.VERSION_NUM] = most_recent_version + 1
        new_record_dict[Fields.CREATED_BY] = user.id_tag

        updated_team = table_class.create(**new_record_dict)

        return updated_team


    ### PRIVATE HELPER METHODS

    def _sanitize_table_dict(self, obj):
        ignored_columns = {'recorded_timestamp'}
        return {k:v for (k, v) in obj.items() if (v and (k not in ignored_columns))}

    def _field_existence(self, obj, fields):
        for field in fields:
            yield getattr(obj, field, None) is not None
