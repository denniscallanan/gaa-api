import random 
import string
import operator

from functools import reduce
from typing import Type, List

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
    pass


class BaseDataModel(Model):
    class Meta:
        database = db

    def to_model(self, model_type):
        return model_type(**get_field_args(self))

    def to_record(self):
        return self.to_model(DTO)

    def to_response_model(self, model_type, success=True):
        status = "success" if success else "failure"
        return ResponseModel(status=status, result=self.to_model(model_type))

    @staticmethod
    def gen_uid(prefix):
        return prefix + '_' + (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12)))


class BaseClient:

    DEFAULT_LIMIT = 10 

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

    def search_and_equal_conjunction(self, table_class, conditions) -> List[BaseDataModel]:
        clauses = [(k == v) for k, v in conditions.items() if v]
        expr = reduce(operator.and_, clauses)
        records = table_class.select().where(expr).limit(BaseClient.DEFAULT_LIMIT).execute()
        latest_records = {}
        for record in records:
            if record.id_tag in latest_records:
                if latest_records[record.id_tag].version_num < record.version_num:
                    latest_records[record.id_tag] = record
            else:
                latest_records[record.id_tag] = record
        return latest_records.values()

    def insert(self, obj, table_class, user) -> BaseDataModel:
        table_dict = self._sanitize_table_dict(dict(obj))
        table_dict[Fields.CREATED_BY] = user.id_tag
        return table_class.create(**table_dict)

    def update(self, id_tag, obj, table_class: Type[BaseDataModel], user) -> BaseDataModel:

        most_recent_record = self.get_by_id(id_tag, table_class)
        most_recent_version = most_recent_record.version_num

        most_recent_record_model = most_recent_record.to_record()
        
        new_record_dict = self.merge(most_recent_record_model, obj)
        new_record_dict[Fields.VERSION_NUM] = most_recent_version + 1
        new_record_dict[Fields.CREATED_BY] = user.id_tag

        return table_class.create(**new_record_dict)


    ### PRIVATE HELPER METHODS

    def _sanitize_table_dict(self, obj):
        ignored_columns = {'recorded_timestamp'}
        return {k:v for (k, v) in obj.items() if (v is not None and (k not in ignored_columns))}
