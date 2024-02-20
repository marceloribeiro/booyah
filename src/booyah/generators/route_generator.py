import os
from jinja2 import Environment, PackageLoader, select_autoescape
from booyah.extensions.string import String
from booyah.generators.base_generator import BaseGenerator
from booyah.generators.helpers.io import print_error, print_success
from booyah.framework import Booyah

class RouteGenerator(BaseGenerator):
    def __init__(self, target_folder):
        self.routes_file_path = os.path.join(target_folder, 'config', 'routes.py')
        self.template_environment = Environment(
            loader=PackageLoader('booyah', 'generators/templates'),
            autoescape=select_autoescape()
        )
    
    def add_resource(self, resource_name):
        if Booyah.is_api:
            template = self.template_environment.get_template('route_resource_api')
        else:
            template = self.template_environment.get_template('route_resource')
        params = { "resource_name": String(resource_name).underscore() }
        content = template.render(**params)
        self.add_code_if_not_exists(content)
    
    def add_code_if_not_exists(self, content):
        try:
            with open(self.routes_file_path, 'r+') as file:
                file_contents = file.read()
                if content in file_contents:
                    print_error(f'Route entry already exists ({content})')
                else:
                    file.write(f"\n{content}")
                    print_success(f"Route entry created!")

        except FileNotFoundError:
            print_error(f'Could not find routes config file ({self.routes_file_path})')
            return False