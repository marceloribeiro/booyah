import os
import argparse
from booyah.generators.helpers.io import print_error, print_success, prompt_override_file
from booyah.generators.helpers.system_check import current_dir_is_booyah_root
from booyah.generators.migration_generator import MigrationGenerator
import booyah.extensions.string

globals()['String'] = booyah.extensions.string.String

def generate_controller(project_module, target_folder, controller_name, actions):
    """
    Create a controller file using the template file controller and replacing placeholder
    Using naming conventions and creating custom actions
    It prompts to override if already exists
    """
    class_name = String(controller_name).classify().pluralize()
    template_path = os.path.join(os.path.dirname(__file__), "templates", "controller")
    target_file = os.path.join(target_folder, class_name.underscore() + '_controller.py')

    is_creation = True
    if os.path.exists(target_file):
        if prompt_override_file(target_file) == False:
            print_error(f'controller already exists ({target_file})')
            return False
        else:
            is_creation = False
            os.remove(target_file)

    actions.append('index')
    actions = list(set(actions))

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    # Replace placeholders using the unique delimiter
    content = template_content.replace('%{controller_name}%', class_name).replace('%{project_module}%', project_module)
    content = content.replace('%{actions}%', '\n    '.join([f"def {action}(self):\n        pass\n" for action in actions]))

    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w") as output_file:
        output_file.write(content)

    print_success(f"controller {('created' if is_creation else 'overridden')} {target_file}")
    return content

def generate_migration(target_folder, migration_name, extra_arguments):
    generator = MigrationGenerator(target_folder, migration_name, extra_arguments)
    generator.perform()

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

    if args.generate == 'controller':
        base_folder = os.path.abspath(os.path.join(os.path.abspath("."), "app/controllers"))
        project_module = os.path.basename(os.getcwd())
        generate_controller(project_module, base_folder, args.resource_name, args.extra_arguments)
    elif args.generate == 'migration':
        base_folder = os.path.abspath(os.path.join(os.path.abspath("."), "db/migrate"))
        generate_migration(base_folder, args.resource_name, args.extra_arguments)
    else:
        print(f"Unknown generator: {args.generate}")