import os
import shutil
from booyah.generators.helpers.io import print_error, prompt_override_file
from jinja2 import Environment, PackageLoader, select_autoescape

class BaseGenerator:
    def booyah_root(self):
        return os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    def should_create_file(self):
        if os.path.exists(self.target_file):
            if prompt_override_file(self.target_file) == False:
                print_error(f'file already exists ({self.target_file})')
                return False
            else:
                os.remove(self.target_file)
                return True
        return True

    def get_template_content(self, template_path, template_name, data):
        template_environment = Environment(
            loader=PackageLoader('booyah', template_path),
            autoescape=select_autoescape()
        )
        template = template_environment.get_template(template_name)
        return template.render(**data)
    
    def copy_folder_tree_with_prompt(self, source_folder, destination_folder):
        try:
            for root, _, files in os.walk(source_folder):
                relative_root = os.path.relpath(root, source_folder)
                destination_root = os.path.join(destination_folder, relative_root)

                os.makedirs(destination_root, exist_ok=True)

                for file_name in files:
                    source_file = os.path.join(root, file_name)
                    destination_file = os.path.join(destination_root, file_name)

                    if os.path.exists(destination_file):
                        user_input = input(f"File '{destination_file}' already exists. Replace (R) or Ignore (I)? ").strip().lower()
                        if user_input == 'r':
                            shutil.copy2(source_file, destination_file)
                            print(f"File replaced '{destination_file}'.")
                        elif user_input == 'i':
                            print(f"Ignoring file '{destination_file}' (user choice: Ignore).")
                        else:
                            print(f"Invalid input: '{user_input}'. File '{source_file}' was not copied.")
                    else:
                        shutil.copy2(source_file, destination_file)

        except FileNotFoundError:
            print("Source folder not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
    def file_extensions_for(self, format):
        if format == 'image':
            return ['.png', '.jpg', '.jpeg', '.ico', '.gif', '.bmp']
        elif format == 'pdf':
            return ['.pdf']
        elif format == 'doc':
            return ['.doc', '.rtf', '.docx', '.pdf', '.txt']
        return ['*']
    
    def is_file_field(self, format):
        return format in ['file', 'image', 'pdf', 'doc', 'attachment']