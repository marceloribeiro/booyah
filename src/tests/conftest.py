import sys
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env.test')
if os.path.isfile(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path, override=False)
print('Spinning up environment [' + os.getenv('BOOYAH_ENV') + ']')

def pytest_configure(config):
    print("****** Running conftest.py ******")
    booyah_path = os.path.join(os.path.dirname(__file__))
    os.environ["ROOT_PROJECT_PATH"] = booyah_path
    os.environ["ROOT_PROJECT"] = ''
    os.environ["PROJECT_NAME"] = 'booyah_test'
    os.environ['BOOYAH_ENV'] = 'test'
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    src_path =  os.path.join(parent_dir, 'src')
    print(f'Adding src dir {src_path} to sys path')
    sys.path.insert(0, src_path)