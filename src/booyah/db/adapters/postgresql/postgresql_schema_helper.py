from booyah.db.adapters.base_adapter import BaseAdapter
from booyah.logger import logger

class PostgresqlSchemaHelper:
    @staticmethod
    def get_instance(force_new=False):
        if not hasattr(PostgresqlSchemaHelper, 'instance') or force_new:
            PostgresqlSchemaHelper.instance = PostgresqlSchemaHelper()
        return PostgresqlSchemaHelper.instance

    def __init__(self):
        self.adapter = BaseAdapter.get_instance()

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

    def create_schema_migrations(self):
        self.create_table('schema_migrations', { 'version': 'varchar(255)' })

    def create_table(self, table_name, table_columns, force=False):
        self.translate_table_columns(table_columns)
        columns = ', '.join([f"{key} {value}" for key, value in table_columns.items()])
        if force:
            query = f"CREATE TABLE {table_name} ({columns})"
        else:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        logger.debug("DB:", query)
        self.adapter.execute(query, False)

    def drop_table(self, table_name):
        self.adapter.execute(f"DROP TABLE IF EXISTS {table_name}", False)

    def add_column(self, table_name, column_name, column_type):
        column_type = self.translate_column_type(column_type)
        self.adapter.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}", False)

    def drop_column(self, table_name, column_name):
        self.adapter.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}", False)

    def rename_column(self, table_name, column_name, new_column_name):
        self.adapter.execute(f"ALTER TABLE {table_name} RENAME COLUMN {column_name} TO {new_column_name}", False)

    def change_column(self, table_name, column_name, column_type):
        column_type = self.translate_column_type(column_type)
        self.adapter.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {column_type} USING {column_name}::{column_type}", False)

    def add_index(self, table_name, column_names, index_name=None):
        column_names_csv = ', '.join(column_names)
        column_names_underscore = '_'.join(column_names)
        if index_name is None:
            index_name = f"{table_name}_{column_names_underscore}_index"
        self.adapter.execute(f"CREATE INDEX {index_name} ON {table_name} ({column_names_csv})", False)

    def remove_index(self, table_name, column_names, index_name=None):
        column_names_underscore = '_'.join(column_names)
        if index_name is None:
            index_name = f"{table_name}_{column_names_underscore}_index"
        self.adapter.execute(f"DROP INDEX {index_name}", False)
