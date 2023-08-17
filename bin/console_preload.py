side_spaces = 20
initial_message = 'Welcome to Booyah Console'

message_length = len(initial_message)
formatted_line = '*' * (side_spaces * 2 + 2) + '*' * message_length

print(formatted_line)
print('*' + ' ' * side_spaces + initial_message + ' ' * side_spaces + '*')
print(formatted_line)

# Load required settings first
import sys
from py_dotenv import read_dotenv
import os
import importlib

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
dotenv_path = os.path.join(parent_dir, 'src', '.env')
read_dotenv(dotenv_path)
src_path =  os.path.join(parent_dir, 'src')
os.chdir(src_path)
sys.path.insert(0, src_path)

# Import libs that require previous settings

def load_models():
    folder_path = os.path.join(src_path, 'lib', 'models')
    ignore_list = ['application_model.py', 'model_query_builder.py']
    file_names = [f for f in os.listdir(folder_path) if f.endswith(".py") and f not in ignore_list and not f.startswith('_')]
    for file_name in file_names:
        module_name = file_name[:-3]
        module = importlib.import_module(f"lib.models.{module_name}")

        for class_name in dir(module):
            cls = getattr(module, class_name)
            globals()[class_name] = cls

def help():
    content = '''
    Booyah console HELP
    -------------------
    Commands list

    No new commands registered
    '''
    print(content)

load_models()