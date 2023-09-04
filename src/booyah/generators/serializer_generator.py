import os
from booyah.extensions.string import String
from booyah.generators.helpers.io import print_success
from booyah.generators.base_generator import BaseGenerator
from jinja2 import Environment, PackageLoader, select_autoescape

class SerializerGenerator(BaseGenerator):
    def __init__(self, target_folder, model_name, attributes):
        self.target_folder = target_folder
        self.model_name = model_name
        self.class_name = String(f"{self.model_name}_serializer").classify()
        self.target_file = os.path.join(self.target_folder, self.class_name.underscore() + '.py')
        self.content = ''
        self.template_environment = Environment(
            loader=PackageLoader('booyah', 'generators/templates'),
            autoescape=select_autoescape()
        )

    def perform(self):
        if not self.should_create_file():
            return False
        self.create_serializer_from_template()

    def load_content(self):
        template = self.template_environment.get_template('serializer_skeleton')
        self.data = {
            "model_name": self.class_name
        }
        self.content = template.render(**self.data)

    def create_serializer_from_template(self):
        self.load_content()
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)
        with open(self.target_file, "w") as output_file:
            output_file.write(self.content)
        print_success(f"serializer created: {self.target_file}")