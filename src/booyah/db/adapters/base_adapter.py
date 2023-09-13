import os
from booyah.extensions.string import String
import subprocess

class BaseAdapter:
    @staticmethod
    def get_instance():
        adapter = String(os.getenv('DB_ADAPTER'))
        module_name = f'booyah.db.adapters.{adapter}.{adapter}_adapter'
        adapter_class = (adapter + '_adapter').camelize()
        adapter_module = __import__(module_name, fromlist=[adapter_class])
        adapter_class = getattr(adapter_module, adapter_class)
        return adapter_class.get_instance()
    
    @staticmethod
    def open_client():
        adapter = os.getenv('DB_ADAPTER', 'postgresql')
        db_client_command = None
        if adapter == 'postgresql':
            db_client_command = f"PGPASSWORD={os.getenv('DB_PASSWORD')} psql -U {os.getenv('DB_USERNAME')} {os.getenv('DB_DATABASE')}"
        if db_client_command:
            subprocess.call(db_client_command, shell=True)

    def create_schema_migrations(self):
        self.create_table('schema_migrations', { 'version': 'varchar(255)' })
    
    def current_version(self):
        query = f"SELECT version from schema_migrations ORDER BY version DESC LIMIT 1"
        result = self.fetch(query)
        if result:
            return int(result[0][0])
        return 0

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