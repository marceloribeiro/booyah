import os
from booyah.generators.helpers.io import print_error, prompt_override_file
from jinja2 import Environment, PackageLoader, select_autoescape

class BaseGenerator:
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