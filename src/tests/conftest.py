import sys
import os
from dotenv import load_dotenv
import psycopg2

dotenv_path = os.path.join(os.path.dirname(__file__), '.env.test')
if os.path.isfile(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path, override=False)
print('Spinning up environment [' + os.getenv('BOOYAH_ENV') + ']')

def reset_database():
    from booyah.framework import Booyah
    db_config = Booyah.env_config['database']
    default_connection = psycopg2.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['username'],
        password=db_config['password'],
        database="postgres",  # Connect to a different database
    )
    with default_connection.cursor() as default_cursor:
        default_cursor.execute("COMMIT")

        default_cursor.execute(f"DROP DATABASE IF EXISTS {db_config['database']}")
        default_cursor.execute(f"CREATE DATABASE {db_config['database']}")
    default_connection.close()

def create_tables():
    from booyah.models.application_model import ApplicationModel
    from booyah.models.session_storage import SessionStorage
    SessionStorage.create_table({
        'id': 'primary_key',
        'session_id': 'string',
        'data': 'text',
        'expires_at': 'datetime',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    })
    SessionStorage.table_columns = None
    print(f'ApplicationModel db {ApplicationModel.db_adapter().database}')
    if ApplicationModel.db_adapter().database == 'postgres':
        raise ValueError('should not use postgres database')

def pytest_sessionstart(session):
    print("****** Running conftest.py ******")
    booyah_path = os.path.join(os.path.dirname(__file__))
    os.environ["ROOT_PROJECT_PATH"] = booyah_path
    os.environ["ROOT_PROJECT"] = ''
    os.environ["PROJECT_NAME"] = 'booyah_test'
    os.environ['BOOYAH_ENV'] = 'test'
    os.environ['BOOYAH_LIB_TEST'] = 'yes'
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    src_path =  os.path.join(parent_dir, 'src')
    print(f'Adding src dir {src_path} to sys path')
    sys.path.insert(0, src_path)
    if not os.getenv('GITHUB_RUNNER') == 'yes':
        reset_database()
    create_tables()