import os
from booyah.extensions.string import String
from booyah.generators.helpers.io import print_error, print_success
from booyah.generators.base_generator import BaseGenerator, ATTACHMENT_TYPES
from booyah.generators.migration_generator import MigrationGenerator
from jinja2 import Environment, PackageLoader, select_autoescape

#  booyah g model user name age:integer bio:text
class ModelGenerator(BaseGenerator):
    def __init__(self, target_folder, model_name, attributes):
        self.target_folder = target_folder
        self.model_name = model_name
        self.model_content = '    pass'
        self.model_imports = ''
        self.attributes = list(set(attributes))
        self.fill_model_content()
        self.attributes = self.prepare_attributes(self.attributes)
        self.class_name = String(self.model_name).classify()
        self.target_file = os.path.join(self.target_folder, self.class_name.underscore() + '.py')
        self.content = ''
        self.template_environment = Environment(
            loader=PackageLoader('booyah', 'generators/templates'),
            autoescape=select_autoescape()
        )

    def perform(self):
        self.generate_migration()
        if not self.should_create_file():
            return False
        self.create_model_from_template()

    def prepare_attributes(self, attributes):
        return [item for item in attributes if ':' not in item or item.split(':')[1] not in ATTACHMENT_TYPES]
    
    def fill_model_content(self):
        has_attachment = False
        for attribute in self.attributes:
            if ':' in attribute:
                name = attribute.split(':')[0]
                bucket = String(name).pluralize()
                format = attribute.split(':')[1]
                if self.is_file_field(format):
                    if not has_attachment:
                        self.model_imports += self.attachment_import_string()
                    has_attachment = True
                    if self.model_content:
                        self.model_content += '\n'
                    self.model_content += self.attachment_config_string(self.model_name, name, format, bucket)

    def generate_migration(self):
        table_name = String(self.model_name).pluralize()
        table_attributes = ['id:primary_key']
        table_attributes += self.attributes
        table_attributes.append('created_at:datetime')
        table_attributes.append('updated_at:datetime')

        MigrationGenerator(
            'db/migrate',
            f"create_table_{table_name}",
            table_attributes
        ).perform()

    def load_content(self):
        template = self.template_environment.get_template('model_skeleton')
        self.data = {
            "model_name": self.class_name,
            "model_content": self.model_content,
            "model_imports": self.model_imports,
        }
        self.content = template.render(**self.data)

    def create_model_from_template(self):
        self.load_content()
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)
        with open(self.target_file, "w") as output_file:
            output_file.write(self.content)
        print_success(f"model created: {self.target_file}")