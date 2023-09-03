import os
import argparse
from booyah.generators.helpers.io import print_error, print_success, prompt_override_file
from booyah.generators.helpers.system_check import current_dir_is_booyah_root
from booyah.generators.migration_generator import MigrationGenerator
from booyah.generators.controller_generator import ControllerGenerator
from booyah.extensions.string import String

def main(args):
    """
    Read args from command line to redirect to correct function
    """
    if not current_dir_is_booyah_root():
        print_error('Not a booyah root project folder')
        return None
    parser = argparse.ArgumentParser(description='Booyah Generator Command')
    parser.add_argument('generate', help='Generate a resource (controller, migration, model, etc.)')
    parser.add_argument('resource_name', help='Resource name (controller name, migration name, model name, etc.)')
    parser.add_argument('extra_arguments', nargs='*', help='List of extra arguments (controller actions, table name, fields, etc.)')

    args = parser.parse_args(args)

    known_generators = [
        'controller',
        'migration'
    ]

    if args.generate not in known_generators:
        print_error(f"Unknown generator: {args.generate}")
        return None

    base_folder = os.path.abspath(os.path.join(os.path.abspath("."), get_target_folder(args.generate)))
    generator_class = String(args.generate).classify() + "Generator"
    generator = globals()[generator_class](base_folder, args.resource_name, args.extra_arguments)
    generator.perform()

def get_target_folder(generate):
    folders = {
        "controller": "app/controllers",
        "migration": "db/migrate"
    }
    return folders[generate]