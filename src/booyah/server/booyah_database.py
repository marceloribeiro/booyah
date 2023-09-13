import psycopg2
from booyah.db.migrate.application_migration import ApplicationMigration
from booyah.db.adapters.base_adapter import BaseAdapter
from booyah.helpers.io import print_success, print_error
from booyah.helpers.io import make_bold, make_blue
import os
import importlib

class BooyahDatabase:
    def __init__(self, environment, params):
        self.environment = environment
        self.adapter = BaseAdapter.get_instance()
        self.params = params
    
    def create_db(self):
        database_to_create = self.adapter.database
        self.adapter.use_system_database()
        try:
            self.adapter.create_database(database_to_create)
            print_success(f'Database {make_blue(make_bold(database_to_create))} created')
        except psycopg2.errors.DuplicateDatabase as e:
            print_error(f'Database {make_blue(make_bold(database_to_create))} already exists!')
    
    def obtain_version_param(self, is_required=True):
        if os.getenv('VERSION'):
            return int(os.getenv('VERSION'))
        elif len(self.params) == 2 and len(self.params[1]) == 14:
            return int(self.params[1])
        if is_required:
            print('Please type a valid version')
    
    def migrate_db(self):
        ApplicationMigration().migrate_to_version(self.obtain_version_param(is_required=False))

    def migrate_up_db(self):
        version = self.obtain_version_param()
        if not version:
            return
        ApplicationMigration().execute_up(version)
    
    def rollback_db(self):
        ApplicationMigration().rollback()

    def migrate_down_db(self):
        version = self.obtain_version_param()
        if not version:
            return
        ApplicationMigration().execute_down(version)
    
    def drop_db(self):
        database_to_drop = self.adapter.database
        self.adapter.use_system_database()
        self.adapter.drop_database(database_to_drop)
        print_success(f'Database {make_blue(make_bold(database_to_drop))} dropped')
    
    def seed_db(self):
        database_to_seed = self.adapter.database
        module = importlib.import_module(f"{os.environ['ROOT_PROJECT']}.db.seed")
        cls = getattr(module, 'Seed')
        cls().run()
        print_success(f'Database {make_blue(make_bold(database_to_seed))} seeded successfully')