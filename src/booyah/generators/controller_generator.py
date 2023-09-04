import os
from booyah.extensions.string import String
from booyah.generators.helpers.io import print_error, print_success
from booyah.generators.base_generator import BaseGenerator
from jinja2 import Environment, PackageLoader, select_autoescape

#  booyah g controller home main contact
class ControllerGenerator(BaseGenerator):
    def __init__(self, target_folder, controller_name, actions, scaffold=False, model_name=None):
        self.target_folder = target_folder
        self.controller_name = f"{controller_name}_controller"
        self.actions = list(set(actions))
        self.scaffold = scaffold
        self.model_name = model_name
        self.class_name = String(self.controller_name).classify()
        self.target_file = os.path.join(self.target_folder, self.class_name.underscore() + '.py')
        self.content = ''
        self.project_module = os.path.basename(os.getcwd())
        self.template_environment = Environment(
            loader=PackageLoader('booyah', 'generators/templates'),
            autoescape=select_autoescape()
        )

    def perform(self):
        if not self.should_create_file():
            return False
        if self.scaffold and len(self.actions) == 0:
            self.actions = ['index', 'show', 'new', 'create', 'edit', 'update', 'destroy']
        self.create_controller_from_template()
        self.create_views_from_template()

    def get_template_data(self):
        data = {
            "controller_name": self.class_name,
            "project_module": self.project_module,
            "model_name": self.model_name,
            "actions": self.actions,
            "action_content": self.get_scaffold_content('action') if self.scaffold else {},
            "view_content": self.get_scaffold_content('view') if self.scaffold else {},
            "scaffold": self.scaffold
        }
        return data

    def load_content(self):
        template = self.template_environment.get_template('controller_skeleton')
        self.data = self.get_template_data()
        self.content = template.render(**self.data)

    def get_scaffold_content(self, mode):
        content = {}

        for action in self.actions:
            skeleton_name = f"{action}_{mode}"
            contents = self.get_template_content(
                'generators/templates/scaffold',
                skeleton_name,
                {
                    "controller_name": self.class_name,
                    "action_name": action,
                    'model_name': self.model_name
                }
            )
            if mode == 'action':
                content[action] = contents
            elif mode == 'view':
                content[action] = contents
        return content

    def create_controller_from_template(self):
        self.load_content()
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)
        with open(self.target_file, "w") as output_file:
            output_file.write(self.content)
        print_success(f"controller created: {self.target_file}")

    def create_views_from_template(self):
        self.load_content()
        for action in self.actions:
            controller_folder = self.class_name.underscore().replace('_controller', '')
            view_file = os.path.join(
                self.target_folder.replace('controllers', f"views/{controller_folder}"),
                action + '.html'
            )
            if os.path.exists(view_file):
                print_error(f'view already exists ({view_file})')
                continue

            template = self.template_environment.get_template('view_skeleton')
            content = template.render(**self.data)
            os.makedirs(os.path.dirname(view_file), exist_ok=True)
            with open(view_file, "w") as output_file:
                output_file.write(content)

            print_success(f"view created: {view_file}")