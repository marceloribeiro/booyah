import os
from booyah.extensions.string import String
from booyah.generators.helpers.io import print_error, print_success
from booyah.generators.base_generator import BaseGenerator
from booyah.generators.model_generator import ModelGenerator
from booyah.generators.serializer_generator import SerializerGenerator
from booyah.generators.controller_generator import ControllerGenerator

#  booyah g scaffold users name age:integer bio:text
class ScaffoldGenerator(BaseGenerator):
    def __init__(self, target_folder, model_name, attributes):
        self.target_folder = target_folder
        self.model_name = String(model_name).singularize()
        self.attributes = list(set(attributes))

    def perform(self):
        self.generate_model()
        self.generate_serializer()
        self.generate_controller()

    def generate_model(self):
        model_generator = ModelGenerator('app/models', self.model_name, self.attributes)
        model_generator.perform()

    def generate_serializer(self):
        model_generator = SerializerGenerator('app/serializers', self.model_name, self.attributes)
        model_generator.perform()

    def generate_controller(self):
        controller_generator = ControllerGenerator(
            'app/controllers',
            self.model_name.pluralize(),
            [],
            scaffold=True,
            model_name=self.model_name,
            model_attributes=self.attributes
        )
        controller_generator.perform()