import os
import sys
from booyah.generators.helpers.system_check import current_dir_is_booyah_root
from booyah.generators.helpers.io import print_error

# If not a booyah root project folder, abort
if not current_dir_is_booyah_root():
    print_error('Not a booyah root project folder')
    quit()

# Console code starts here -----------------------------------------------------
from py_dotenv import read_dotenv
import os
import importlib

read_dotenv('.env')

def configure():
    """
    Load extensions to console
    """
    from booyah.extensions.string import String
    globals()['String'] = String

def load_models():
    """
    Load all models from lib/models, except some system files
    """
    models_folder = os.path.join('app', 'models')
    ignore_list = ['application_model.py', 'model_query_builder.py']
    file_names = [f for f in os.listdir(models_folder) if f.endswith(".py") and f not in ignore_list and not f.startswith('_')]
    for file_name in file_names:
        module_name = file_name[:-3]
        module = importlib.import_module(f"booyah.models.{module_name}")

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