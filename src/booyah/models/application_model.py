from booyah.db.adapters.base_adapter import BaseAdapter
from booyah.models.model_query_builder import ModelQueryBuilder
from booyah.extensions.string import String
from booyah.observers.application_model_observer import ApplicationModelObserver
import json
from datetime import datetime
import os
import importlib

class ApplicationModel:
    validates = []
    accessors = []
    _has_one = []
    table_columns = None

    def __init__(self, attributes={}):
        self.errors = []
        self.fill_attributes(attributes, from_init=True)

    @classmethod
    def custom_validates(klass):
        if not hasattr(klass, '_custom_validates') and not klass is ApplicationModel:
            klass._custom_validates = []
        return klass._custom_validates
    
    def fill_attributes(self, attributes, from_init=False, ignore_none=False):
        additional_attributes = self.__class__.accessors + [item['name'] for item in self.__class__._has_one]
        if from_init:
            for column in self.get_table_columns():
                setattr(self, column, None)
                setattr(self, f"{column}_was", None)
            for accessor in additional_attributes:
                setattr(self, accessor, None)

        if not attributes:
            return

        for key in attributes:
            if (key in self.get_table_columns() or key in additional_attributes) and (ignore_none == False or attributes[key] != None):
                setattr(self, key, attributes[key])
                if from_init and key in self.get_table_columns():
                    setattr(self, f"{key}_was", attributes[key])

    @classmethod
    def db_adapter(self):
        return BaseAdapter.get_instance()

    @classmethod
    def table_name(self):
        return String(self.__name__).underscore().pluralize()

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
        return ModelQueryBuilder(self)

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
    def where(self, *args):
        return self.query_builder().where(*args)

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
        if self.is_new_record():
            self.insert()
        else:
            self.update()
        self.save_relations()
        self.after_save()
        self.reload(keep_accessors=True)
        return self
    
    def save_relations(self):
        for relation in [item['name'] for item in self.__class__._has_one]:
            value = getattr(self, relation)
            if value != None and value.id == None:
                value.save()

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


    def reload(self, keep_accessors=False):
        if self.id:
            dicttionary = self.__class__.find(self.id).to_dict()

            if keep_accessors:
                for accessor_name in self.__class__.accessors:
                    dicttionary[accessor_name] = getattr(self, accessor_name)
            self.__init__(dicttionary)

    def is_new_record(self):
        return not hasattr(self, 'id') or self.id == None

    def insert(self, validate=True):
        if validate and not self.valid():
            return False
        self.before_save()
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
        self.updated_at = datetime.now()
        self.before_save()
        self.before_update()
        self_attributes = self.to_dict()
        data = self.db_adapter().update(self.table_name(), self.id, self_attributes)
        self.after_update()
        return self

    def patch_update(self, attributes = None):
        self.before_update()
        self.fill_attributes(attributes, ignore_none=True)
        self.updated_at = datetime.now()
        self_attributes = self.to_dict()
        if attributes != None:
            to_update = {key: value for key, value in attributes.items() if key in self.get_table_columns()}
            for key in to_update:
                if attributes.get(key) != None:
                    self_attributes[key] = attributes[key]
        data = self.db_adapter().update(self.table_name(), self.id, self_attributes)
        self.after_update()
        return self

    def destroy(self):
        self.before_destroy()
        self.apply_destroy_dependent_action()
        data = self.db_adapter().delete(self.table_name(), self.id)
        deleted_id = data[0]
        self.after_destroy()
        return deleted_id
    
    def apply_destroy_dependent_action(self):
        for item in self.__class__._has_one:
            value = getattr(self, item['name'])
            if value:
                if item.get('dependent') == 'destroy':
                    value.destroy()
                elif item.get('dependent') == 'nullify':
                    setattr(value, item['foreign_key'], None)
                    value.save()

    def valid(self):
        self.before_validation()
        self.errors = []

        if not self.__class__.validates and not self.__class__.custom_validates:
            result = self.relations_valid()
            self.after_validation()            
            return result
        for v in self.__class__.validates:
            self.perform_attribute_validations(v)

        for v in self.__class__.custom_validates():
            v(self)
        result = self.relations_valid()
        self.after_validation()            
        return False if self.errors else True
    
    def relations_valid(self):
        is_valid = True
        for relation_name in [item['name'] for item in self.__class__._has_one]:
            value = getattr(self, relation_name)
            if value != None and value.id == None:
                if not value.valid():
                    is_valid = False
                    self.errors.append(f"{relation_name} invalid: {', '.join(value.errors)}")
        return is_valid

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
    
    def import_model(self, model_name, globals_ref):
        model_name_str = String(model_name)
        class_name = model_name_str.classify()
        if class_name in globals_ref:
            return
        module_name = f"{os.getenv('ROOT_PROJECT')}.app.models.{model_name_str.underscore()}"
        module = importlib.import_module(module_name)
        klass = getattr(module, class_name)
        globals_ref[class_name] = klass