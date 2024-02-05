from booyah.generators.helpers.system_check import current_dir_is_booyah_root
from booyah.generators.helpers.io import print_error

# If not a booyah root project folder, abort
if not current_dir_is_booyah_root():
    print_error('Not a booyah root project folder')
    quit()

# Ready to start console (valid folder) -----------------------------------------------------
import sys
import os
import importlib

class BooyahConsole:

    def configure(self):
        """
        Load extensions to console
        """
        from booyah.extensions.string import String
        from booyah.framework import Booyah
        globals()['String'] = String
        globals()['Booyah'] = Booyah
        sys.path.append(os.path.dirname(Booyah.root))

    def load_models(self):
        """
        Load all models from lib/models, except some system files
        """
        models_folder = os.path.join('app', 'models')
        ignore_list = ['application_model.py', 'model_query_builder.py']
        file_names = [f for f in os.listdir(models_folder) if f.endswith(".py") and f not in ignore_list and not f.startswith('_')]
        for file_name in file_names:
            module_name = file_name[:-3]
            module = importlib.reload(importlib.import_module(f"{Booyah.folder_name}.app.models.{module_name}"))

            for class_name in dir(module):
                cls = getattr(module, class_name)
                globals()[class_name] = cls

    def welcome_message(self):
        side_spaces = 20
        initial_message = 'Welcome to Booyah Console'

        message_length = len(initial_message)
        formatted_line = '*' * (side_spaces * 2 + 2) + '*' * message_length

        print(formatted_line)
        print('*' + ' ' * side_spaces + initial_message + ' ' * side_spaces + '*')
        print(formatted_line)

    def start(self):
        self.configure()
        self.load_models()

# Public commands below

def help():
    content = '''
    Booyah console HELP
    -------------------
    Commands list

    reload() - Will reload the env and booyah modules
    '''
    print(content)

def reload():
    # env should be reloaded first, cause the libs may need to use it
    global _initial_global_keys

    current_global_keys = set(globals().keys())
    keys_to_remove = current_global_keys - _initial_global_keys

    for key in keys_to_remove:
        if key != '_initial_global_keys':
            del globals()[key]

    __console.start()

# Start console class, public methods should be declared before setting _initial_global_keys 
__console = BooyahConsole()
__console.welcome_message()

# Everything loaded to global until here will be kept as default/not realoading
_initial_global_keys = set(globals().keys())
__console.start()