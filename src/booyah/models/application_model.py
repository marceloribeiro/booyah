from booyah.db.adapters.base_adapter import BaseAdapter
from booyah.models.model_query_builder import ModelQueryBuilder
from booyah.extensions.string import String
from booyah.observers.application_model_observer import ApplicationModelObserver
import json
from datetime import datetime

class ApplicationModel:
    validates = []
    table_columns = None
    _query_builder = None

    def __init__(self, attributes={}):
        self.errors = []
        self.fill_attributes(attributes, from_init=True)
        self.configure_static_var()

    @classmethod
    def configure_static_var(cls):
        cls.custom_validates = []
    
    def fill_attributes(self, attributes, from_init=False, ignore_none=False):
        if from_init:
            for column in self.get_table_columns():
                setattr(self, column, None)
                setattr(self, f"{column}_was", None)
        if not attributes:
            return

        for key in attributes:
            if key in self.get_table_columns() and (ignore_none == False or attributes[key] != None):
                setattr(self, key, attributes[key])
                if from_init:
                    setattr(self, f"{key}_was", attributes[key])

    @classmethod
    def db_adapter(self):
        return BaseAdapter.get_instance()

    @classmethod
    def table_name(self):
        return self.__name__.lower() + 's'

    @classmethod
    def get_table_columns(self):
        if self.table_columns is None:
            self.table_columns = self.db_adapter().get_table_columns(self.table_name())
            self.table_columns.sort()

        return self.table_columns

    @classmethod
    def create_table(self, table_columns):
        self.db_adapter().create_table(self.table_name(), table_columns)

    @classmethod
    def drop_table(self):
        self.db_adapter().drop_table(self.table_name())

    @classmethod
    def query_builder(self):
        if self._query_builder != None:
            return self._query_builder
        self._query_builder = ModelQueryBuilder(self)
        return self._query_builder

    @classmethod
    def count(self):
        return self.query_builder().count()

    @classmethod
    def all(self):
        return self.query_builder().all()

    @classmethod
    def find(self, id):
        try:
            user = self.query_builder().find(id).results()[0]
            return user
        except IndexError:
            return None

    @classmethod
    def where(self, column, value):
        return self.query_builder().where(column, value)

    @classmethod
    def exists(self, conditions):
        return self.query_builder().exists(conditions)

    @classmethod
    def join(self, table, condition):
        return self.query_builder().join(table, condition)

    @classmethod
    def left_join(self, table, condition):
        return self.query_builder().left_join(table, condition)

    @classmethod
    def right_join(self, table, condition):
        return self.query_builder().right_join(table, condition)

    @classmethod
    def order(self, order):
        return self.query_builder().order(order)

    @classmethod
    def group(self, group):
        return self.query_builder().group(group)

    @classmethod
    def limit(self, limit):
        return self.query_builder().limit(limit)

    @classmethod
    def offset(self, offset):
        return self.query_builder().offset(offset)

    @classmethod
    def page(self, page):
        return self.query_builder().page(page)

    @classmethod
    def per_page(self, per_page):
        return self.query_builder().per_page(per_page)

    @classmethod
    def first(self):
        return self.query_builder().first()

    @classmethod
    def last(self):
        return self.query_builder().last()

    @classmethod
    def create(self, attributes):
        self.model = self(attributes)
        self.model.save()
        return self.model

    def serialized_attribute(self, attribute):
        if hasattr(self, attribute):
            return getattr(self, attribute)
        return None

    def save(self):
        if not self.valid():
            return False
        self.before_save()
        if self.is_new_record():
            self.insert()
        else:
            self.update(validate=False)
        self.reload()
        self.after_save()
        return self

    def before_validation(self):
        self.run_callbacks('before_validation')
    
    def after_validation(self):
        self.run_callbacks('after_validation')

    def before_save(self):
        self.run_callbacks('before_save')
    
    def after_save(self):
        self.run_callbacks('after_save')

    def before_create(self):
        self.run_callbacks('before_create')
    
    def after_create(self):
        self.run_callbacks('after_create')
    
    def before_update(self):
        self.run_callbacks('before_update')
    
    def after_update(self):
        self.run_callbacks('after_update')
    
    def before_destroy(self):
        self.run_callbacks('before_destroy')
    
    def after_destroy(self):
        self.run_callbacks('after_destroy')

    def run_callbacks(self, callback_type):
        callbacks = ApplicationModelObserver.callbacks.get(callback_type)
        class_name = self.__class__.__name__

        if not callbacks:
            return
        
        if ApplicationModelObserver.callbacks[callback_type].get(class_name):
            callback_configs = sorted(
                ApplicationModelObserver.callbacks[callback_type][class_name],
                key=lambda x:x['sorting_index']
            )
            for callback_config in callback_configs:
                callback = callback_config.get('block')
                if type(callback) == str:
                    callback = getattr(self, callback)
                    callback()        


    def reload(self):
        if self.id:
            self.__init__(self.__class__.find(self.id).to_dict())

    def is_new_record(self):
        return not hasattr(self, 'id') or self.id == None

    def insert(self):
        self.before_create()
        data = self.db_adapter().insert(self.table_name(), self.compact_to_dict())
        self.id = data[0]
        self.created_at = data[1]
        self.updated_at = data[2]
        self.after_create()
        return self

    def update(self, attributes = None, validate=True):
        self.fill_attributes(attributes)
        if validate and not self.valid():
            return False
        self.before_update()
        self_attributes = self.to_dict()
        data = self.db_adapter().update(self.table_name(), self.id, self_attributes)
        self.updated_at = data[0]
        self.after_update()
        return self

    def patch_update(self, attributes = None):
        self.before_update()
        self.fill_attributes(attributes, ignore_none=True)
        self_attributes = self.to_dict()
        if attributes != None:
            to_update = {key: value for key, value in attributes.items() if key in self.get_table_columns()}
            for key in to_update:
                if attributes.get(key) != None:
                    self_attributes[key] = attributes[key]
        data = self.db_adapter().update(self.table_name(), self.id, self_attributes)
        self.updated_at = data[0]
        self.after_update()
        return self

    def destroy(self):
        self.before_destroy()
        data = self.db_adapter().delete(self.table_name(), self.id)
        deleted_id = data[0]
        self.after_destroy()
        return deleted_id

    def valid(self):
        self.before_validation()
        self.errors = []

        if not self.__class__.validates and not self.__class__.custom_validates:
            self.after_validation()            
            return True
        for v in self.__class__.validates:
            self.perform_attribute_validations(v)

        for v in self.__class__.custom_validates:
            v(self)
        self.after_validation()            
        return False if self.errors else True

    def perform_attribute_validations(self, attribute_validations):
        attribute = list(attribute_validations.keys())[0]
        validations = attribute_validations[attribute]
        for validation in validations:
            self.perform_validation(attribute, validation, validations[validation])

    def perform_validation(self, attribute, validation, validation_value):
        validator_class = String(f"{validation}_validator").camelize()
        validator_class = getattr(__import__(f"booyah.validators.{validator_class.underscore()}", fromlist=[validator_class]), validator_class)
        validator = validator_class(self, attribute, validation_value)
        validator.validate()

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