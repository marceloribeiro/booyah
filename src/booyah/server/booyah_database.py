import psycopg2
from booyah.db.migrate.application_migration import ApplicationMigration
from booyah.db.adapters.base_adapter import BaseAdapter
from booyah.helpers.io import print_success, print_error
from booyah.helpers.io import make_bold, make_blue
import os
import importlib

class BooyahDatabase:
    def __init__(self, environment):
        self.environment = environment
        self.adapter = BaseAdapter.get_instance()
    
    def create_db(self):
        database_to_create = self.adapter.database
        self.adapter.use_system_database()
        try:
            self.adapter.create_database(database_to_create)
            print_success(f'Database {make_blue(make_bold(database_to_create))} created')
        except psycopg2.errors.DuplicateDatabase as e:
            print_error(f'Database {make_blue(make_bold(database_to_create))} already exists!')
    
    def migrate_db(self):
        ApplicationMigration().migrate_all()
    
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