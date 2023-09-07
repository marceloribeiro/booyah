# First step, adding helper folder to sys path to be able to import functions
import os
import sys
import argparse
import subprocess
import re
from booyah.generators.helpers.io import print_error, print_success, prompt_override_file
from booyah.generators.helpers.system_check import current_dir_is_booyah_root, prompt_replace
from booyah.generators.base_generator import BaseGenerator
import shutil

import booyah.extensions.string
globals()['String'] = booyah.extensions.string.String

class NewGenerator(BaseGenerator):
    def __init__(self, args):
        self.booyah_root = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
        parser = argparse.ArgumentParser(description='Creating New Booyah Project')
        parser.add_argument("project_name", help="The project name")
        args = parser.parse_args(args)
        if not args.project_name.strip():
            raise ValueError("Please type the project name")
        
        self.folder_name = String(args.project_name.strip()).underscore()
        self.folder_path = os.path.join(os.getcwd(), self.folder_name)
        self.project_name = self.folder_name

    def perform(self):
        if not self.validate():
            return None

        self.copy_booyah_version()
        self.create_project()

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

        source_folder = os.path.realpath(os.path.join(self.booyah_root, 'generators', 'templates', 'generate_new'))
        destination_folder = self.folder_name

        self.copy_folder_tree_with_prompt(source_folder, destination_folder)
        
        shutil.copy(os.path.join(source_folder, 'env'), os.path.join(destination_folder, '.env'))
        shutil.copy(os.path.join(source_folder, 'application.py'), os.path.join(destination_folder, 'application.py'))
        shutil.copy(os.path.join(source_folder, '__init__.py'), os.path.join(destination_folder, '__init__.py'))
        shutil.copy(os.path.join(source_folder, 'requirements.txt'), os.path.join(destination_folder, 'requirements.txt'))

        print(f"Project '{self.project_name}' created successfully.")