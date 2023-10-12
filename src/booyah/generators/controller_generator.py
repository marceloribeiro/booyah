import os
from booyah.extensions.string import String
from booyah.generators.helpers.io import print_error, print_success
from booyah.generators.base_generator import BaseGenerator
from jinja2 import Environment, PackageLoader, select_autoescape

#  booyah g controller home main contact
class ControllerGenerator(BaseGenerator):
    def __init__(self, target_folder, controller_name, actions, scaffold=False, model_name=None, model_attributes=[]):
        self.has_attachment = False
        self.target_folder = target_folder
        self.controller_name = f"{controller_name}_controller"
        self.actions = list(set(actions))
        self.scaffold = scaffold
        self.model_name = model_name
        self.model_attributes = self.format_attributes(model_attributes)
        self.permit_attributes = self.permit_attributes(model_attributes)
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
        self.load_content()
        self.create_controller_from_template()
        self.create_views_from_template()

    def format_attributes(self, attributes):
        formatted = []
        for attribute in attributes:
            if ':' not in attribute:
                name = attribute
                format = 'string'
            else:
                name = attribute.split(':')[0]
                format = attribute.split(':')[1]
            formatted.append({
                "name": String(name),
                "format": String(format),
                "field_type": String(self.get_field_type(format)),
                "extra": String(self.get_field_extra(format))
            })
        return formatted

    def permit_attributes(self, attributes):
        formatted = []
        for attribute in attributes:
            if ':' not in attribute:
                name = attribute
                format = 'string'
            else:
                name = attribute.split(':')[0]
                format = attribute.split(':')[1]
            formatted.append(String(name))
            if String(self.get_field_type(format)) == 'file_field':
                formatted.append(String(f'_destroy_{name}'))

        return formatted

    def get_template_data(self):
        data = {
            "controller_name": self.class_name,
            "project_module": self.project_module,
            "model_name": self.model_name,
            "actions": self.actions,
            "action_content": self.get_scaffold_content('action') if self.scaffold else {},
            "view_content": self.get_scaffold_content('view') if self.scaffold else {},
            'model_attributes': self.model_attributes if self.scaffold else [],
            "model_attributes_names": self.get_model_attributes_names(),
            "permit_attributes": self.get_permit_attributes_names(),
            "scaffold": self.scaffold
        }
        return data

    def load_content(self):
        template = self.template_environment.get_template('controller_skeleton')
        self.data = self.get_template_data()
        self.content = template.render(**self.data)

    def get_scaffold_content(self, mode):
        content = {}

        for action in (self.actions + ['form', 'form_multipart']):
            if mode == 'view' and action in ['create', 'update', 'destroy']:
                continue

            skeleton_name = f"{action}_{mode}"
            contents = self.get_template_content(
                'generators/templates/scaffold',
                skeleton_name,
                {
                    "controller_name": self.class_name,
                    "action_name": action,
                    'model_name': self.model_name,
                    'model_attributes': self.model_attributes if self.scaffold else [],
                    "model_attributes_names": self.get_model_attributes_names()
                }
            )
            if mode == 'action':
                content[action] = contents
            elif mode == 'view':
                content[action] = contents
        return content

    def create_controller_from_template(self):
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)
        with open(self.target_file, "w") as output_file:
            output_file.write(self.content)
        print_success(f"controller created: {self.target_file}")

    def create_view_for_action(self, action, template_name=None):
        if not template_name:
            template_name = action
        if self.scaffold and action in ['create', 'update', 'destroy']:
            return

        controller_folder = self.class_name.underscore().replace('_controller', '')
        view_file = os.path.join(
            self.target_folder.replace('controllers', f"views/{controller_folder}"),
            action + '.html'
        )
        if os.path.exists(view_file):
            print_error(f'view already exists ({view_file})')
            return

        if self.scaffold:
            content = self.get_scaffold_content('view')[template_name]
        else:
            template_name = f"scaffold/{template_name}_view" if self.scaffold else 'view_skeleton'
            template = self.template_environment.get_template(template_name)
            content = template.render(**self.data)

        os.makedirs(os.path.dirname(view_file), exist_ok=True)
        with open(view_file, "w") as output_file:
            output_file.write(content)
        print_success(f"view created: {view_file}")

    def create_views_from_template(self):
        for action in self.actions:
            self.create_view_for_action(action)
        if self.has_attachment:
            self.create_view_for_action('form', template_name='form_multipart')
        else:
            self.create_view_for_action('form')

    def get_model_attributes_names(self):
        if not self.model_name:
            return ''
        return ', '.join([f"'{attribute['name']}'" for attribute in self.model_attributes])

    def get_permit_attributes_names(self):
        if not self.permit_attributes:
            return ''
        return ', '.join([f"'{attribute}'" for attribute in self.permit_attributes])

    def get_field_extra(self, field_type):
        if field_type in ['image', 'pdf', 'doc']:
            return ','.join(self.file_extensions_for(field_type))
        elif field_type in ['file', 'attachment']:
            return '*'

    def get_field_type(self, field_type):
        if self.is_file_field(field_type):
            self.has_attachment = True
            return 'file_field'

        options = {
            'string': 'text_field',
            'text': 'textarea_field',
            'integer': 'number_field',
            'float': 'number_field',
            'boolean': 'checkbox_field',
            'date': 'date_field',
            'time': 'time_field',
            'datetime': 'datetime_field',
        }
        if field_type in options:
            return options[field_type]
        return 'text_field'