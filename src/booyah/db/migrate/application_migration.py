from booyah.db.adapters.base_adapter import BaseAdapter
from booyah.extensions.string import String
import os

class ApplicationMigration:
    def __init__(self, version=None):
        self.should_run_up = True
        self.should_run_down = True
        self.success_up = False
        self.success_down = False
        self.adapter = BaseAdapter.get_instance()
        self.version = version
        self.already_created_schema = False

    def migrations_folder(self):
        return f"{os.getenv('ROOT_PROJECT_PATH')}/db/migrate"

    def get_migrations(self):
        migrations = []
        files = os.listdir(self.migrations_folder())
        files.sort()
        for file in files:
            if file.endswith('.py') and not file.startswith('application_migration') and not file.startswith('__init__'):
                migrations.append(file)
        return migrations

    def migrate_to_version(self, to_version):
        if not to_version:
            self.migrate_all()
            return
        
        all_migrations = self.get_migrations()
        current_version = self.adapter.current_version()
        
        if current_version < to_version:
            for migration in all_migrations:
                version = int(migration.split('_')[0])
                if version > current_version and version <= to_version:
                    self.migrate(migration, version)
        else:
            all_migrations.reverse()
            should_set_version_zero = True
            for migration in all_migrations:
                version = int(migration.split('_')[0])

                already_migrated = current_version >= version
                should_undo = version > to_version

                if already_migrated and should_undo:
                    self.migrate_down(migration, version)
                    self.version = version
                    self.delete_version()
                elif already_migrated:
                    should_set_version_zero = False
                    current_version = version
                    break
            self.version = current_version if not should_set_version_zero else 0

    def migrate_all(self):
        current_version = self.adapter.current_version()
        migrations = self.get_migrations()
        for migration in migrations:
            version = int(migration.split('_')[0])
            if current_version < version:
                self.migrate(migration, version)
    
    def rollback(self):
        current_version = self.adapter.current_version()
        if not current_version:
            return
        all_migrations = self.get_migrations()
        all_migrations.reverse()
        for migration in all_migrations:
            version = int(migration.split('_')[0])
            if version == current_version:
                self.migrate_down(migration, version)
                self.version = version
                self.delete_version()

    def get_migration_class(self, migration, migration_class_name):
        migration_module = __import__(f'{os.environ["ROOT_PROJECT"]}.db.migrate.{migration.split(".")[0]}', fromlist=[migration_class_name])
        migration_class = getattr(migration_module, migration_class_name)
        return migration_class
    
    def get_migration_by_version(self, version):
        all_migrations = self.get_migrations()

        for migration in all_migrations:
            if int(migration.split('_')[0]) == version:
                return migration
        print(f'Could not find migration with the version {version}')

    def execute_up(self, version):
        migration = self.get_migration_by_version(version)
        if migration:
            self.migrate(migration, version)

    def execute_down(self, version):
        migration = self.get_migration_by_version(version)
        if migration:
            self.migrate_down(migration, version)

    def migrate(self, migration, version):
        migration_name = String(migration.split('.')[0].replace(f"{version}_", ''))
        migration_class_name = migration_name.camelize()
        migration_class = self.get_migration_class(migration, migration_class_name)
        migration_class(version).up()

    def migrate_down(self, migration, version):
        migration_name = String(migration.split('.')[0].replace(f"{version}_", ''))
        migration_class_name = migration_name.camelize()
        migration_class = self.get_migration_class(migration, migration_class_name)
        migration_class(version).down()

    def create_schema_migrations(self):
        if not self.already_created_schema:
            self.already_created_schema = True
            self.adapter.create_schema_migrations()

    def migration_has_been_run(self):
        return self.adapter.migration_has_been_run(self.version)

    def before_up(self):
        self.create_schema_migrations()
        self.should_run_up = not self.migration_has_been_run()

    def after_up(self):
        if self.success_up:
            print("Saving version")
            self.save_version()
        self.adapter.close_connection()

    def before_down(self):
        self.should_run_down = self.migration_has_been_run()

    def after_down(self):
        if self.success_down:
            self.delete_version()
        self.adapter.close_connection()

    def up(self, block):
        self.before_up()
        if self.should_run_up:
            print("running migration")
            block()
            print("done")
            self.success_up = True
        self.after_up()

    def down(self, block):
        self.before_down()
        if self.should_run_down:
            block()
            self.success_down = True
        self.after_down()

    def save_version(self):
        self.adapter.save_version(self.version)

    def delete_version(self):
        self.adapter.delete_version(self.version)

    def create_table(self, table_name, table_columns):
        self.adapter.create_table(table_name, table_columns)

    def drop_table(self, table_name):
        self.adapter.drop_table(table_name)

    def add_column(self, table_name, data):
        for column_name, column_type in data.items():
            self.adapter.add_column(table_name, column_name, column_type)

    def drop_column(self, table_name, column_name):
        self.adapter.drop_column(table_name, column_name)

    def rename_column(self, table_name, column_name, new_column_name):
        self.adapter.rename_column(table_name, column_name, new_column_name)

    def change_column(self, table_name, column_name, column_type):
        self.adapter.change_column(table_name, column_name, column_type)

    def add_index(self, table_name, column_name):
        self.adapter.add_index(table_name, column_name)

    def remove_index(self, table_name, column_name):
        self.adapter.remove_index(table_name, column_name)