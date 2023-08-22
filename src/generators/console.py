# First step, adding helper folder to sys path to be able to import functions
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from helpers.system_check import current_dir_is_booyah_root
from helpers.io import print_error

# If not a booyah root project folder, abort
if not current_dir_is_booyah_root():
    print_error('Not a booyah root project folder')
    quit()

# Console code starts here -----------------------------------------------------
from py_dotenv import read_dotenv
import os
import importlib

parent_dir = os.path.abspath(".")
dotenv_path = os.path.join(parent_dir, 'src', '.env')
read_dotenv(dotenv_path)
src_path = os.path.join(parent_dir, 'src')

def configure():
    os.chdir(src_path)
    sys.path.insert(0, src_path)
    import lib.extensions.string
    globals()['String'] = lib.extensions.string.String

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

def welcome_message():
    side_spaces = 20
    initial_message = 'Welcome to Booyah Console'

    message_length = len(initial_message)
    formatted_line = '*' * (side_spaces * 2 + 2) + '*' * message_length

    print(formatted_line)
    print('*' + ' ' * side_spaces + initial_message + ' ' * side_spaces + '*')
    print(formatted_line)

configure()
load_models()
welcome_message()