import os
import shutil
from booyah.generators.helpers.io import print_error, print_success
from booyah.generators.base_generator import BaseGenerator
from booyah.generators.helpers.path import new_migration_file_path

MIGRATION_TEMPLATE_NAME = 'create_table_session_storage.py'

#  booyah g session install
class SessionGenerator(BaseGenerator):
    def __init__(self, target_folder, command, extra_arguments):
        self.target_folder = target_folder
        self.command = command

    def perform(self):
        if self.command == 'install':
            self.install()
        else:
            print(f'Command not found {self.command}')
    
    def install(self):
        print('Installing session')
        files_in_folder = os.listdir(self.target_folder)
        
        already_exists = any(file.endswith(MIGRATION_TEMPLATE_NAME) for file in files_in_folder)

        if already_exists:
            print_error(f"Already have the session migration ({MIGRATION_TEMPLATE_NAME}).")
        else:
            source_file = os.path.join(self.booyah_root(), 'generators', 'templates', MIGRATION_TEMPLATE_NAME)
            target_file = new_migration_file_path(self.target_folder, MIGRATION_TEMPLATE_NAME)
            shutil.copy2(source_file, target_file)
            print_success('Migration for session created successfully!')
        