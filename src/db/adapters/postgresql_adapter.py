import psycopg
import os
from datetime import datetime

class PostgresqlAdapter:
    @staticmethod
    def get_instance():
        if not hasattr(PostgresqlAdapter, 'instance'):
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

    def execute(self, query):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def fetch(self, query):
        self.connect()
        cursor = self.connection.cursor()
        print("DEBUG DB: ", query)
        try:
            cursor.execute(query)
        except Exception as e:
            print("ERROR: ", e)
            self.close_connection()
            return []
        records = cursor.fetchall()
        return records

    def table_columns(self, table_name):
        self.connect()
        cursor = self.connection.cursor()
        query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        print("DEBUG DB: ", query)
        cursor.execute(query)
        columns = [item for row in cursor.fetchall() for item in row]
        return columns

    def last_insert_id(self, table_name):
        query = f"SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1"
        records = self.fetch(query)
        if len(records) == 0:
            return None
        return records[0][0]

    def insert(self, table_name, attributes):
        if attributes.get('created_at') == None:
            attributes['created_at'] = datetime.now()
        if attributes.get('updated_at') == None:
            attributes['updated_at'] = datetime.now()

        columns = ', '.join(attributes.keys())
        values = ', '.join([f"'{value}'" for value in attributes.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        print("DEBUG DB: ", query)
        self.execute(query)
        return self.last_insert_id(table_name)

    def update(self, table_name, id, attributes):
        if attributes.get('updated_at') == None:
            attributes['updated_at'] = datetime.now()
        self.format_attributes(attributes)

        values = ', '.join([f"{key} = {value}" for key, value in attributes.items()])
        query = f"UPDATE {table_name} SET {values} WHERE id = {id}"
        print("DEBUG DB: ", query)
        self.execute(query)

    def delete(self, table_name, id):
        query = f"DELETE FROM {table_name} WHERE id = {id}"
        print("DEBUG DB: ", query)
        self.execute(query)

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
            elif value == None:
                attributes[key] = 'NULL'
            else:
                attributes[key] = str(value)