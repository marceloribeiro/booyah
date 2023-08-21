import argparse
import os
from .helpers.string_functions import to_class_name, convert_to_snake_case
from .helpers.io import print_error, print_success, prompt_override_file
from .helpers.system_check import current_dir_is_booyah_root

def generate_controller(target_folder, controller_name, actions):
    class_name = to_class_name(controller_name, plural=True)
    template_path = os.path.join(os.path.dirname(__file__), "templates", "controller")
    target_file = os.path.join(target_folder, convert_to_snake_case(class_name) + '_controller.py')
    
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
    content = template_content.replace('%{controller_name}%', class_name)
    content = content.replace('%{actions}%', '\n    '.join([f"def {action}(self):\n        pass\n" for action in actions]))

    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w") as output_file:
        output_file.write(content)

    print_success(f"controller {('created' if is_creation else 'overridden')}")
    return content


def main(args):
    if not current_dir_is_booyah_root():
        print_error('Not a booyah root project folder')
        return None
    parser = argparse.ArgumentParser(description='Booyah Generator Command')
    parser.add_argument('generate', help='Generate a resource (controller, model, etc.)')
    parser.add_argument('resource', help='Resource name (controller name, model name, etc.)')
    parser.add_argument('actions', nargs='*', help='List of actions')

    args = parser.parse_args(args)

    if args.generate == 'controller':
        base_folder = os.path.abspath(os.path.join(os.path.abspath("."), "src/app/controllers"))
        generate_controller(base_folder, args.resource, args.actions)
    else:
        print(f"Unknown generator: {args.generate}")