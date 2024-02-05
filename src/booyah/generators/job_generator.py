import os
from booyah.extensions.string import String
from booyah.generators.helpers.io import print_error, print_success
from booyah.generators.base_generator import BaseGenerator
from booyah.generators.attachments_generator import file_extensions_for, is_file_field
from jinja2 import Environment, PackageLoader, select_autoescape

#  booyah g job job_name task1 task2 task3
class JobGenerator(BaseGenerator):
    def __init__(self, target_folder, job_name, tasks):
        self.target_folder = target_folder
        self.job_name = String(f"{job_name}_job")
        self.tasks = self.remove_duplicates_preserve_order(tasks)
        self.target_file = os.path.join(self.target_folder, self.job_name.underscore() + '.py')
        self.project_module = os.path.basename(os.getcwd())
        self.template_environment = Environment(
            loader=PackageLoader('booyah', 'generators/templates'),
            autoescape=select_autoescape()
        )

    def perform(self):
        if not self.should_create_file():
            return False
        self.load_content()
        self.task_template = self.template_environment.get_template('task_skeleton')
        self.create_job_from_template()

    def load_content(self):
        template = self.template_environment.get_template('job_skeleton')
        data = {}
        self.content = template.render(**data)

    def get_template_data(self, task):
        return {
            "task_name": task,
        }

    def create_job_from_template(self):
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)
        with open(self.target_file, "w") as output_file:
            output_file.write(self.content)
            for task in self.tasks:
                data = self.get_template_data(task)
                task_content = self.task_template.render(**data)
                output_file.write("\n\n" + task_content)
        print_success(f"job created: {self.target_file}")