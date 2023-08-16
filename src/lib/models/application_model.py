from db.adapters.base_adapter import BaseAdapter
from lib.models.model_query_builder import ModelQueryBuilder
import json

class ApplicationModel:
    table_columns = None
    query_builder = None

    @classmethod
    def db_adapter(self):
        return BaseAdapter.get_instance()

    @classmethod
    def table_name(self):
        return self.__name__.lower() + 's'

    @classmethod
    def get_table_columns(self):
        if self.table_columns == None:
            self.table_columns = self.db_adapter().table_columns(self.table_name())
        return self.table_columns

    @classmethod
    def load_query_builder(self):
        if self.query_builder != None:
            return self.query_builder
        self.query_builder = ModelQueryBuilder(self)
        return self.query_builder

    @classmethod
    def all(self):
        self.load_query_builder()
        return self.query_builder.all().results()

    @classmethod
    def find(self, id):
        self.load_query_builder()
        return self.query_builder.find(id).results()[0]

    @classmethod
    def where(self, column, value):
        self.load_query_builder()
        return self.query_builder.where(column, value).results()

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
        self.reload()

    def reload(self):
        if self.id:
            self.__init__(self.__class__.find(self.id).to_dict())

    def is_new_record(self):
        return not hasattr(self, 'id')

    def insert(self):
        self.id = self.db_adapter().insert(self.table_name(), self.compact_to_dict())

    def update(self, attributes = None):
        self_attributes = self.to_dict()
        if attributes != None:
            self_attributes.update(attributes)
        self.db_adapter().update(self.table_name(), self.id, self_attributes)
        self.reload()

    def patch_update(self, attributes = None):
        self_attributes = self.to_dict()
        if attributes != None:
            for key in attributes:
                if attributes.get(key) != None:
                    self_attributes[key] = attributes[key]
        self.db_adapter().update(self.table_name(), self.id, self_attributes)
        self.reload()

    def destroy(self):
        self.db_adapter().delete(self.table_name(), self.id)

    def get_table_values(self):
        return [ self.serialized_attribute(column) for column in self.get_table_columns() ]

    def to_dict(self):
        dicttionary = { column: self.serialized_attribute(column) for column in self.get_table_columns() }
        return json.loads(json.dumps(dicttionary, default=str))

    def to_json(self):
        return json.dumps(self.to_dict(), default=str)