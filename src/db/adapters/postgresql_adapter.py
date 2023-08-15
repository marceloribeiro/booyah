import psycopg
import json
import os

GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
STORAGE_BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME')


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

    def execute(self, query):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def fetch(self, query):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    def table_columns(self, table_name):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        columns = [item for row in cursor.fetchall() for item in row]
        return columns