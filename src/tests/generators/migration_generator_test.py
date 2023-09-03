import os
import json
from booyah.generators.migration_generator import MigrationGenerator

class TestMigrationGenerator:
    def test_intance_inits_with_default_values(self):
        migration_generator = MigrationGenerator('target_folder', 'migration_name', 'fields')

        assert migration_generator.target_folder == 'target_folder'
        assert migration_generator.migration_name == 'migration_name'
        assert migration_generator.fields == 'fields'
        assert migration_generator.class_name == 'MigrationName'
        assert migration_generator.template_path == os.path.join(os.path.dirname(__file__)).replace('/tests/generators', '') + '/booyah/generators/templates/migration'
        assert migration_generator.target_file == f"target_folder/{migration_generator.current_datetime}_migration_name.py"
        assert migration_generator.table_name == ''
        assert migration_generator.content == ''
        assert migration_generator._formatted_fields == ''

    def test_formatted_fields_returns_formatted_fields(self):
        migration_generator = MigrationGenerator('target_folder', 'migration_name', ['name:string', 'age:int'])
        fields_json = json.dumps(migration_generator.formatted_fields()).replace(' ', '').replace('\\n','').replace('"', '')
        assert fields_json == "{'name':'string','age':'int'}"

    def test_load_table_name_sets_table_name(self):
        migration_generator = MigrationGenerator('target_folder', 'create_table_users', 'fields')
        migration_generator.load_table_name()
        assert migration_generator.table_name == 'users'

        migration_generator = MigrationGenerator('target_folder', 'add_name_to_users_table', 'fields')
        migration_generator.load_table_name()
        assert migration_generator.table_name == 'users'

    def test_load_content(self):
        migration_generator = MigrationGenerator('target_folder', 'create_table_users', ['name:string', 'age:int'])
        migration_generator.load_content()
        assert migration_generator.content == self.create_sample_content()

        migration_generator = MigrationGenerator('target_folder', 'add_name_to_users_table', ['name:string'])
        migration_generator.load_content()
        assert migration_generator.content == self.add_column_sample_content()

    def test_up_content(self):
        migration_generator = MigrationGenerator('target_folder', 'create_table_users', ['name:string', 'age:int'])
        assert migration_generator.up_content() == self.up_sample_create_table_content()

        migration_generator = MigrationGenerator('target_folder', 'add_name_to_users_table', ['name:string'])
        assert migration_generator.up_content() == self.up_sample_add_column_content()

    def test_down_content(self):
        migration_generator = MigrationGenerator('target_folder', 'create_table_users', ['name:string', 'age:int'])
        assert migration_generator.down_content() == self.down_sample_create_table_content()

        migration_generator = MigrationGenerator('target_folder', 'add_name_to_users_table', ['name:string'])
        assert migration_generator.down_content() == self.down_sample_add_column_content()

    def test_is_create_table_migration(self):
        migration_generator = MigrationGenerator('target_folder', 'create_table_users', 'fields')
        assert migration_generator.is_create_table_migration() == True

        migration_generator = MigrationGenerator('target_folder', 'add_name_to_users_table', 'fields')
        assert migration_generator.is_create_table_migration() == False

    def test_is_add_column_to_table_migration(self):
        migration_generator = MigrationGenerator('target_folder', 'create_table_users', 'fields')
        assert migration_generator.is_add_column_to_table_migration() == False

        migration_generator = MigrationGenerator('target_folder', 'add_name_to_users_table', 'fields')
        assert migration_generator.is_add_column_to_table_migration() == True

    def create_sample_content(self):
        return """from booyah.db.migrate.application_migration import ApplicationMigration

class CreateTableUser(ApplicationMigration):
    def up(self):
        super().up(lambda: self.create_table('users', {
            'name': 'string',
            'age': 'int'
        }))

    def down(self):
        super().down(lambda: self.drop_table('users'))"""

    def add_column_sample_content(self):
        return """from booyah.db.migrate.application_migration import ApplicationMigration

class AddNameToUsersTable(ApplicationMigration):
    def up(self):
        super().up(lambda: self.add_column('users', {
            'name': 'string'
        }))

    def down(self):
        super().down(lambda: self.remove_column('users', {
            'name': 'string'
        }))"""

    def up_sample_create_table_content(self):
        return """super().up(lambda: self.create_table('users', {
            'name': 'string',
            'age': 'int'
        }))"""

    def up_sample_add_column_content(self):
        return """super().up(lambda: self.add_column('users', {
            'name': 'string'
        }))"""

    def down_sample_create_table_content(self):
        return """super().down(lambda: self.drop_table('users'))"""

    def down_sample_add_column_content(self):
        return """super().down(lambda: self.remove_column('users', {
            'name': 'string'
        }))"""