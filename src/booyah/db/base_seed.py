import os
import importlib

class BaseSeed:
    def load_models(self, globals_ref):
        """
        Load all models from lib/models, except some system files
        """
        models_folder = os.path.join('app', 'models')
        ignore_list = ['application_model.py', 'model_query_builder.py']
        file_names = [f for f in os.listdir(models_folder) if f.endswith(".py") and f not in ignore_list and not f.startswith('_')]
        for file_name in file_names:
            module_name = file_name[:-3]
            module = importlib.import_module(f"{os.environ['ROOT_PROJECT']}.app.models.{module_name}")

            for class_name in dir(module):
                cls = getattr(module, class_name)
                globals_ref[class_name] = cls
    
    def run(self):
        pass