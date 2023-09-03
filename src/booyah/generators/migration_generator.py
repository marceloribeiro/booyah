import os
from booyah.extensions.string import String
from booyah.generators.helpers.io import print_error, print_success, prompt_override_file
from datetime import datetime

#  booyah g migration create_table_comments comments user_id:integer title content:text
class MigrationGenerator:
    def __init__(self, target_folder, migration_name, fields):
        current_datetime = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
        self.target_folder = target_folder
        self.migration_name = migration_name
        self.fields = fields
        self.class_name = String(self.migration_name).classify().pluralize()
        self.template_path = os.path.join(os.path.dirname(__file__), "templates", "migration")
        self.target_file = os.path.join(self.target_folder, current_datetime + '_' + self.class_name.underscore() + '.py')
        self.table_name = ''
        self.content = ''
        self._formatted_fields = ''

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
      else:
        self.table_name = self.migration_name.replace('add_', '').replace('_to_', '_').replace('_table', '')

    def load_content(self):
      self.load_table_name()

      template_content = ''
      with open(self.template_path, "r") as template_file:
          template_content = template_file.read()
      self.content = template_content.replace('%{migration_name}%', self.class_name)

      self.content = self.content.replace('%{up_content}%', self.up_content())
      self.content = self.content.replace('%{down_content}%', self.down_content())

    def up_content(self):
        if self.is_create_table_migration():
            return self.create_table_content()
        elif self.is_add_column_to_table_migration():
            return self.add_column_content()
        else:
            return ""

    def down_content(self):
        if self.is_create_table_migration():
            return self.drop_table_content()
        elif self.is_add_column_to_table_migration():
            return self.remove_column_content()
        else:
            return ""

    def is_create_table_migration(self):
        return self.migration_name.startswith('create_table_')

    def is_add_column_to_table_migration(self):
        return self.migration_name.startswith('add_') and self.migration_name.endswith('_to_')

    def create_table_content(self):
        return f"super().up(lambda: self.create_table('{self.table_name}', {self.formatted_fields()}))"

    def drop_table_content(self):
        return f"super().down(lambda: self.drop_table('{self.table_name}'))"

    def add_column_content(self):
        return f"super().up(lambda: self.add_column('{self.table_name}', '{self.formatted_fields()}'))"

    def remove_column_content(self):
        return f"super().down(lambda: self.remove_column('{self.table_name}', '{self.formatted_fields()}'))"

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
      else:
        self.load_content()
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)
        with open(self.target_file, "w") as output_file:
            output_file.write(self.content)

        print_success(f"migration created: {self.target_file}")
        return self.content