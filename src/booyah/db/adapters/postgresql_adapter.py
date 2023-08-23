import psycopg
import os
from datetime import datetime
from booyah.logger import logger

class PostgresqlAdapter:
    @staticmethod
    def get_instance(force_new=False):
        if not hasattr(PostgresqlAdapter, 'instance') or force_new:
            PostgresqlAdapter.instance = PostgresqlAdapter()
        return PostgresqlAdapter.instance

    def __init__(self):
      self.load_config()

    def load_config(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.user = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_DATABASE')
        self.connection = None

    def connect(self):
        if self.connection:
            return self.connection
        self.connection = psycopg.connect(
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

    def execute(self, query, expect_result=True):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        if expect_result:
            result = cursor.fetchone()
            self.connection.commit()
            return result
        return None

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

    def table_columns(self, table_name):
        self.connect()
        cursor = self.connection.cursor()
        query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        logger.debug("DB:", query, color='blue', bold=True)
        cursor.execute(query)
        columns = [item for row in cursor.fetchall() for item in row]
        columns.sort()
        return columns

    def create_table(self, table_name, table_columns):
        self.translate_table_columns(table_columns)
        self.connect()
        cursor = self.connection.cursor()
        columns = ', '.join([f"{key} {value}" for key, value in table_columns.items()])
        query = f"CREATE TABLE {table_name} ({columns})"
        logger.debug("DB:", query)
        cursor.execute(query)
        self.connection.commit()

    def drop_table(self, table_name):
        self.connect()
        cursor = self.connection.cursor()
        query = f"DROP TABLE IF EXISTS {table_name}"
        logger.debug("DB:", query)
        cursor.execute(query)
        self.connection.commit()

    def insert(self, table_name, attributes):
        if attributes.get('created_at') is None:
            attributes['created_at'] = datetime.now()
        if attributes.get('updated_at') is None:
            attributes['updated_at'] = datetime.now()
        self.format_attributes(attributes)

        columns = ', '.join(attributes.keys())
        values = ', '.join([f"{value}" for value in attributes.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING id, created_at, updated_at"
        logger.debug("DB:", query, color='green', bold=True)
        return self.execute(query)

    def update(self, table_name, id, attributes):
        if attributes.get('updated_at') is None:
            attributes['updated_at'] = datetime.now()
        if 'created_at' in attributes:
            attributes.pop('created_at')

        self.format_attributes(attributes)

        values = ', '.join([f"{key} = {value}" for key, value in attributes.items()])
        query = f"UPDATE {table_name} SET {values} WHERE id = {id} returning updated_at"
        logger.debug("DB:", query, color='yellow', bold=True)
        return self.execute(query)

    def delete(self, table_name, id):
        query = f"DELETE FROM {table_name} WHERE id = {id} returning id"
        logger.debug("DB:", query, color='red', bold=True)
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

    def translate_table_columns(self, table_columns):
        for name, type in table_columns.items():
            table_columns[name] = self.translate_column_type(type)

    def column_types(self):
        return {
            'primary_key': 'SERIAL PRIMARY KEY',
            'string': 'VARCHAR(255)',
            'text': 'TEXT',
            'integer': 'INTEGER',
            'float': 'FLOAT',
            'decimal': 'DECIMAL',
            'datetime': 'TIMESTAMP',
            'time': 'TIME',
            'date': 'DATE',
            'binary': 'BYTEA',
            'boolean': 'BOOLEAN',
            'json': 'JSON',
            'jsonb': 'JSONB',
            'uuid': 'UUID',
            'inet': 'INET',
        }

    def translate_column_type(self, type):
        return self.column_types().get(type, 'VARCHAR(255)')