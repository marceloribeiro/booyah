import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from datetime import datetime
from booyah.logger import logger
from booyah.db.adapters.postgresql.postgresql_schema_helper import PostgresqlSchemaHelper
from booyah.framework import Booyah

class PostgresqlAdapter:
    @staticmethod
    def get_instance(force_new=False):
        if not hasattr(PostgresqlAdapter, 'instance') or force_new:
            PostgresqlAdapter.instance = PostgresqlAdapter()
        return PostgresqlAdapter.instance

    def __init__(self):
      self.load_config()

    def load_config(self):
        db_config = Booyah.env_config['database']
        self.host = db_config.get('host')
        self.port = db_config.get('port')
        self.user = db_config.get('username')
        self.password = db_config.get('password')
        self.database = db_config.get('database')
        self.connection = None
    
    def create_database(self, database_name):
        self.execute_without_transaction(f'CREATE DATABASE {database_name}')
    
    def drop_database(self, database_name):
        self.execute_without_transaction(f'DROP DATABASE IF EXISTS {database_name}')
    
    def use_system_database(self):
        self.database = 'postgres'
    
    def rollback(self):
        if self.connection:
            self.connection.rollback()

    def connect(self):
        if self.connection:
            return self.connection
        logger.debug(f"Connecting to host: {self.host} port: {self.port} dbname: {self.database}")
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.database
        )
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_without_transaction(self, query, expect_result=True):
        self.connect()
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = self.connection.cursor()
        logger.debug("DB (no transaction):", query, color='blue')
        cursor.execute(query)
        cursor.close()
        self.close_connection()

    def execute(self, query, expect_result=True):
        try:
            self.connect()
            cursor = self.connection.cursor()
            color = 'blue'
            bold = False
            upper_query = query.upper()
            if upper_query.startswith("INSERT INTO"):
                color = 'green'
                bold = True
            elif upper_query.startswith("UPDATE"):
                color = 'yellow'
                bold = True
            elif upper_query.startswith("DELETE"):
                color = 'red'
                bold = True
            logger.debug("DB:", query, color=color, bold=bold)
            cursor.execute(query)
            result = None
            if expect_result:
                result = cursor.fetchone()
            self.connection.commit()
        except psycopg2.Error as e:
            if isinstance(e, psycopg2.errors.InFailedSqlTransaction):
                self.rollback()
                print("Transaction rolled back due to error:", e)
            else:
                raise e
        return result

    def fetch(self, query):
        self.connect()
        cursor = self.connection.cursor()
        logger.debug("DB:", query, color='blue')
        try:
            cursor.execute(query)
        except Exception as e:
            logger.fatal("DB FETCH:", e)
            self.close_connection()
            return []
        records = cursor.fetchall()
        return records

    def insert(self, table_name, attributes):
        if attributes.get('created_at') is None:
            attributes['created_at'] = datetime.now()
        if attributes.get('updated_at') is None:
            attributes['updated_at'] = datetime.now()
        self.format_attributes(attributes)

        columns = ', '.join(attributes.keys())
        values = ', '.join([f"{value}" for value in attributes.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING id, created_at, updated_at"
        return self.execute(query)

    def update(self, table_name, id, attributes):
        if attributes.get('updated_at') is None:
            attributes['updated_at'] = datetime.now()
        if 'created_at' in attributes:
            attributes.pop('created_at')

        self.format_attributes(attributes)

        values = ', '.join([f"{key} = {value}" for key, value in attributes.items()])
        query = f"UPDATE {table_name} SET {values} WHERE id = {id} returning updated_at"
        return self.execute(query)

    def delete(self, table_name, id):
        query = f"DELETE FROM {table_name} WHERE id = {id} returning id"
        return self.execute(query)

    def format_attributes(self, attributes):
        for key, value in attributes.items():
            if type(value) == str:
                attributes[key] = f"'{value}'"
            elif type(value) == bool:
                attributes[key] = str(value).lower()
            elif type(value) == datetime:
                attributes[key] = f"'{value}'"
            elif type(value) == int:
                attributes[key] = str(value)
            elif value is None:
                attributes[key] = 'NULL'
            else:
                attributes[key] = str(value)

    def schema_helper(self):
        return PostgresqlSchemaHelper.get_instance()

    def create_schema_migrations(self):
        self.schema_helper().create_schema_migrations()

    def migration_has_been_run(self, version):
        query = f"SELECT version from schema_migrations where version = '{version}'"
        result = self.fetch(query)
        if result:
            return True
        return False

    def save_version(self, version):
        query = f"INSERT INTO schema_migrations (version) VALUES ('{version}')"
        self.execute(query, False)

    def delete_version(self, version):
        query = f"DELETE FROM schema_migrations WHERE version = '{version}'"
        self.execute(query, False)
    
    def current_version(self):
        query = f"SELECT version from schema_migrations ORDER BY version DESC LIMIT 1"
        result = self.fetch(query)
        if result:
            return int(result[0][0])
        return 0

    def get_table_columns(self, table_name):
        items = self.fetch(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        columns = [item for row in items for item in row]
        columns.sort()
        return columns

    # Delegated to schema helper
    def create_table(self, table_name, table_columns):
        self.schema_helper().create_table(table_name, table_columns)

    def drop_table(self, table_name):
        self.schema_helper().drop_table(table_name)

    def add_column(self, table_name, column_name, column_type):
        self.schema_helper().add_column(table_name, column_name, column_type)

    def drop_column(self, table_name, column_name):
        self.schema_helper().drop_column(table_name, column_name)

    def rename_column(self, table_name, column_name, new_column_name):
        self.schema_helper().rename_column(table_name, column_name, new_column_name)

    def change_column(self, table_name, column_name, column_type):
        self.schema_helper().change_column(table_name, column_name, column_type)

    def add_index(self, table_name, column_names, index_name=None):
        self.schema_helper().add_index(table_name, column_names, index_name=index_name)

    def remove_index(self, table_name, column_name):
        self.schema_helper().remove_index(table_name, column_name)