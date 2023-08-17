from db.adapters.base_adapter import BaseAdapter
from lib.models.model_query_builder import ModelQueryBuilder
import json

class ApplicationModel:
    table_columns = None
    _query_builder = None

    @classmethod
    def db_adapter(self):
        return BaseAdapter.get_instance()

    @classmethod
    def table_name(self):
        return self.__name__.lower() + 's'

    @classmethod
    def get_table_columns(self):
        if self.table_columns is None:
            self.table_columns = self.db_adapter().table_columns(self.table_name())
        return self.table_columns

    @classmethod
    def query_builder(self):
        if self._query_builder != None:
            return self._query_builder
        self._query_builder = ModelQueryBuilder(self)
        return self._query_builder

    @classmethod
    def all(self):
        return self.query_builder().all()

    @classmethod
    def find(self, id):
        return self.query_builder().find(id).results()[0]

    @classmethod
    def where(self, column, value):
        return self.query_builder().where(column, value)

    @classmethod
    def first(self):
        return self.query_builder().first()

    @classmethod
    def create(self, attributes):
        self.model = self(attributes)
        self.model.save()
        return self.model

    def __init__(self, attributes):
        for key in attributes:
            if key in self.get_table_columns():
                setattr(self, key, attributes[key])

    def serialized_attribute(self, attribute):
        if hasattr(self, attribute):
            return getattr(self, attribute)
        return None

    def save(self):
        if self.is_new_record():
            self.insert()
        else:
            self.update()

    def reload(self):
        if self.id:
            self.__init__(self.__class__.find(self.id).to_dict())

    def is_new_record(self):
        return not hasattr(self, 'id')

    def insert(self):
        data = self.db_adapter().insert(self.table_name(), self.compact_to_dict())
        self.id = data[0]
        self.created_at = data[1]
        self.updated_at = data[2]

    def update(self, attributes = None):
        self_attributes = self.to_dict()
        if attributes != None:
            self_attributes.update(attributes)
        data = self.db_adapter().update(self.table_name(), self.id, self_attributes)
        self.updated_at = data[0]

    def patch_update(self, attributes = None):
        self_attributes = self.to_dict()
        if attributes != None:
            for key in attributes:
                if attributes.get(key) != None:
                    self_attributes[key] = attributes[key]
        data = self.db_adapter().update(self.table_name(), self.id, self_attributes)
        self.updated_at = data[0]

    def destroy(self):
        data = self.db_adapter().delete(self.table_name(), self.id)
        deleted_id = data[0]
        return deleted_id

    def get_table_values(self):
        return [ self.serialized_attribute(column) for column in self.get_table_columns() ]

    def compact_to_dict(self):
        dicttionary = { column: self.serialized_attribute(column) for column in self.get_table_columns() }
        return { k: v for k, v in dicttionary.items() if v is not None }

    def to_dict(self):
        dicttionary = { column: self.serialized_attribute(column) for column in self.get_table_columns() }
        return json.loads(json.dumps(dicttionary, default=str))

    def to_json(self):
        return json.dumps(self.to_dict(), default=str)