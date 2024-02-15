# First step, adding helper folder to sys path to be able to import functions
import os
import argparse
import subprocess
import re
from booyah.generators.helpers.io import print_error, print_success
from booyah.generators.helpers.system_check import current_dir_is_booyah_root, prompt_replace
from booyah.generators.base_generator import BaseGenerator
from jinja2 import Environment, PackageLoader, select_autoescape
import shutil
from datetime import datetime
from booyah.extensions.string import String

import booyah.extensions.string
globals()['String'] = booyah.extensions.string.String

class NewGenerator(BaseGenerator):
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='Creating New Booyah Project')
        parser.add_argument("project_name", help="The project name")
        parser.add_argument("--api", action="store_true", help="Include API setup")

        args = parser.parse_args(args)
        if not args.project_name.strip():
            raise ValueError("Please type the project name")
        
        self.is_api = args.api
        self.folder_name = String(args.project_name.strip()).underscore()
        self.folder_path = os.path.join(os.getcwd(), self.folder_name)
        self.project_name = self.folder_name
        self.project_module = String(self.project_name).underscore()
        self.template_environment = Environment(
            loader=PackageLoader('booyah', 'generators/templates'),
            autoescape=select_autoescape()
        )

    def perform(self):
        if not self.validate():
            return None

        self.copy_booyah_version()
        self.create_project()
        self.fill_file_vars()

    def validate(self):
        if current_dir_is_booyah_root():
            print_error('Already are or inside a booyah root project folder')
            return None

        if os.path.exists(self.folder_path):
            response = input(f"The folder '{self.folder_path}' already exists. Are you sure you want to use this folder to create the project? (yes/no): ")
            if response.lower() != "yes":
                return False

        return True

    def copy_booyah_version(self):
        """
        Create .booyah_version file with the current booyah version (used to check if the folder is a booyah project)
        """
        target_folder = self.folder_path
        target_file_path = os.path.join(target_folder, '.booyah_version')
        if prompt_replace(target_file_path):
            os.makedirs(target_folder, exist_ok=True)
            with open(target_file_path, "w") as file:
                file.write(self.get_booyah_version())

    def get_booyah_version(self):
        try:
            output = subprocess.check_output(["pip", "show", "booyah"]).decode("utf-8")
            version_line = re.search(r"Version: (.+)", output)
            if version_line:
                return version_line.group(1)
            else:
                return 'booyah pip not found'
        except subprocess.CalledProcessError:
            return 'booyah pip not found'

    def create_project(self):
        """
        Copy folders required to run a new booyah project
        """

        template_folder = 'generate_new' if not self.is_api else 'generate_new_api'
        application_template = 'application_yml' if not self.is_api else 'api_application_yml'
        source_folder = os.path.realpath(os.path.join(self.booyah_root(), 'generators', 'templates', template_folder))
        destination_folder = self.folder_name

        self.copy_folder_tree_with_prompt(source_folder, destination_folder)

        os.rename(os.path.join(destination_folder, 'env'), os.path.join(destination_folder, '.env'))
        shutil.copy(os.path.join(source_folder, '__init__.py'), os.path.join(destination_folder, '__init__.py'))
        shutil.copy(os.path.join(source_folder, 'requirements.txt'), os.path.join(destination_folder, 'requirements.txt'))

        self.render_template('application', os.path.join(destination_folder, 'application.py'))
        self.render_template(application_template, os.path.join(destination_folder, 'config', 'application.yml'))
        print_success(f"Project '{self.project_name}' created successfully.")

    def render_template(self, source_template, destination_file):
        template = self.template_environment.get_template(source_template)
        template_data = { "project_module": self.project_module, "project_name": self.project_name }
        file_content = template.render(**template_data)

        with open(destination_file, "w") as output_file:
            output_file.write(file_content)

    def fill_file_vars(self):
        if self.is_api:
            replace_settings = {}
        else:
            replace_settings = {
                os.path.join(self.folder_name, 'app', 'views', 'layouts', 'application.html'): [
                    ["{{ PROJECT_YEAR_HERE }}", f"{datetime.now().year}"]
                ]
            }
        for file_path, search_replace_list in replace_settings.items():
            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()

                for search_str, replace_str in search_replace_list:
                    file_content = file_content.replace(search_str, replace_str)

                with open(file_path, 'w') as file:
                    file.write(file_content)

            except Exception as e:
                print(f"Error updating {file_path}: {str(e)}")
