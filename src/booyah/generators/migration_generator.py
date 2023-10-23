import os
import re
from datetime import datetime
from booyah.extensions.string import String
from booyah.generators.helpers.io import print_error, print_success
from jinja2 import Environment, PackageLoader, select_autoescape
from booyah.generators.base_generator import BaseGenerator, ATTACHMENT_TYPES

#  booyah g migration create_table_comments comments user_id:integer title content:text
class MigrationGenerator(BaseGenerator):
    def __init__(self, target_folder, migration_name, fields):
        self.current_datetime = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
        self.target_folder = target_folder
        self.migration_name = String(migration_name).underscore()
        self.fields = self.prepare_fields(fields)
        self.class_name = String(self.migration_name).classify()
        self.target_file = os.path.join(self.target_folder, self.current_datetime + '_' + self.class_name.underscore() + '.py')
        self.table_name = ''
        self.content = ''
        self._formatted_fields = ''
        self.template_environment = Environment(
            loader=PackageLoader('booyah', 'generators/templates'),
            autoescape=select_autoescape()
        )

    def prepare_fields(self, fields):
        attachment_fields = [item for item in fields if ':' in item and item.split(':')[1] in ATTACHMENT_TYPES]
        if attachment_fields:
            self.add_attachment_code(attachment_fields)
        return [item for item in fields if item not in attachment_fields]

    def add_attachment_code(self, attachment_fields):
        self.load_table_name()
        model_file_name = String(self.table_name).singularize().underscore()
        model_class_name = model_file_name.classify()
        model_file_path = os.path.abspath(f"{self.target_folder}/../../app/models/{model_file_name}.py")
        if not os.path.isfile(model_file_path):
            print_error(f'Model file not found {model_file_path}')
            return
        for attachment_field in attachment_fields:
            name = attachment_field.split(':')[0]
            format = attachment_field.split(':')[1]
            search_for = self.attachment_config_prefix(model_class_name, name)
            with open(model_file_path, "r") as file:
                file_contents = file.read()
            if re.sub(r'\s', '', search_for) not in re.sub(r'\s', '', file_contents):
                has_import = re.sub(r'\s', '', self.attachment_import_string()) in re.sub(r'\s', '', file_contents)
                attachment_code = f"\n{self.attachment_config_string(model_class_name, name, format, name)}"
                if not has_import:
                    with open(model_file_path, 'w') as file:
                        file.write(f"{self.attachment_import_string()}\n{file_contents}{attachment_code}")
                else:
                    with open(model_file_path, "a") as file:
                        file.write(attachment_code)
                print_success(f'Successfully configured attachment {name} with type {format} for {model_class_name}')
            else:
                print_error(f'{model_class_name} already has an attachment named {name}')
    
    def formatted_fields(self):
      if self._formatted_fields:
        return self._formatted_fields

      if self.fields:
        self._formatted_fields = map(lambda field: field.split(':'), self.fields)
        self._formatted_fields = (',\n' + 12 * ' ').join(map(lambda field: f"'{field[0]}': '{field[1] if len(field) > 1 else 'string'}'", self._formatted_fields))
        self._formatted_fields = '{\n' +  + 12 * ' ' + self._formatted_fields + '\n' +  8 * ' ' +'}' if self._formatted_fields else '{}'

      return self._formatted_fields

    def load_table_name(self):
      if self.is_create_table_migration():
        self.table_name = self.migration_name.replace('create_table_', '')
      elif self.is_add_column_to_table_migration():
        parts = self.migration_name.split('_to_')
        self.table_name = parts[1].replace('_table', '')
      else:
        self.table_name = ''

    def load_content(self):
        self.load_table_name()
        template = self.template_environment.get_template('migration_skeleton')
        self.data = {
            "migration_name": self.class_name,
            "up_content": self.up_content(),
            "down_content": self.down_content()
        }
        self.content = template.render(**self.data)

    def up_content(self):
        self.load_table_name()

        if self.is_create_table_migration():
            return self.create_table_content()
        elif self.is_add_column_to_table_migration():
            return self.add_column_content()
        else:
            return ""

    def down_content(self):
        self.load_table_name()

        if self.is_create_table_migration():
            return self.drop_table_content()
        elif self.is_add_column_to_table_migration():
            return self.remove_column_content()
        else:
            return ""

    def is_create_table_migration(self):
        return self.migration_name.startswith('create_table_')

    def is_add_column_to_table_migration(self):
        return self.migration_name.startswith('add_') and ('_to_' in self.migration_name)

    def create_table_content(self):
        return f"super().up(lambda: self.create_table('{self.table_name}', {self.formatted_fields()}))"

    def drop_table_content(self):
        return f"super().down(lambda: self.drop_table('{self.table_name}'))"

    def add_column_content(self):
        return f"super().up(lambda: self.add_column('{self.table_name}', {self.formatted_fields()}))"

    def remove_column_content(self):
        return f"super().down(lambda: self.remove_column('{self.table_name}', {self.formatted_fields()}))"

    def is_existing_migration(self):
        existing_migrations = []
        for file in os.listdir(self.target_folder):
            if file.endswith(".py"):
                parts = file.split('_')
                parts.pop(0)
                existing_migration = ('_').join(parts).replace('.py', '')
                existing_migrations.append(existing_migration)
        return self.migration_name in existing_migrations

    def perform(self):
        if self.is_existing_migration():
            print_error(f"There is already a migration with the name {self.migration_name}")
            return False
        elif not self.fields:
            print_error(f"There are no fields to create a migration file!")
            return False
        else:
            self.create_file_from_template()

    def create_file_from_template(self):
        self.load_content()
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)
        with open(self.target_file, "w") as output_file:
            output_file.write(self.content)

        print_success(f"migration created: {self.target_file}")
        return self.content