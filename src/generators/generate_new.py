# First step, adding helper folder to sys path to be able to import functions
import os
import sys
import shutil
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from helpers.io import print_error, print_success, prompt_override_file
from helpers.system_check import current_dir_is_booyah_root, booyah_src_path, prompt_replace

sys.path.append(booyah_src_path())
import lib.extensions.string
globals()['String'] = lib.extensions.string.String

def main(args):
    if current_dir_is_booyah_root():
        print_error('Already are or inside a booyah root project folder')
        return None
    parser = argparse.ArgumentParser(description='Creating New Booyah Project')
    parser.add_argument("project_name", help="The project name")
    args = parser.parse_args(args)
    if not args.project_name.strip():
        print_error('Please type the project name')
        return

    folder_name = String(args.project_name.strip()).underscore()
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    if os.path.exists(folder_path):
        response = input(f"The folder '{folder_path}' already exists. Are you sure you want to use this folder to create the project? (yes/no): ")
        if response.lower() != "yes":
            exit()
    copy_booyah_version(folder_path)
    print(f'Project created at: {folder_name}')

def copy_booyah_version(target_folder):
    source_file_path = os.path.realpath(os.path.join(current_dir, '../../.booyah_version'))
    target_file_path = os.path.join(target_folder, '.booyah_version')
    if prompt_replace(target_file_path):
        os.makedirs(target_folder, exist_ok=True)
        shutil.copy2(source_file_path, target_file_path)