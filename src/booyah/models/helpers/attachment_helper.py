import os
from booyah.models.file import File
import uuid
import types

def save_attachments(self):
    for attachment in self._attachments:
        options = getattr(self, f"_{attachment}_options")
        current_value = getattr(self, attachment)
        previous_value = None if not hasattr(self, f"{attachment}_was") else getattr(self, f"{attachment}_was")
        if type(previous_value) is File:
            previous_value = None
        if type(current_value) is File:
            if previous_value:
                self.delete_file(previous_value, options)
            random_filename = str(uuid.uuid4())
            extension = str(current_value).split('.')[-1]
            full_file_name = f"{random_filename}.{extension}"

            if os.getenv('BOOYAH_ENV') != 'production':
                target_path = os.path.join(self.attachment_folder(options), full_file_name)
                self.save_local_attachment(str(current_value), target_path)
                setattr(self, attachment, full_file_name)
        elif current_value == '' and previous_value:
            breakpoint()
            self.delete_file(previous_value, options)

def validate_attachments(self):
    for attachment in self._attachments:
        options = getattr(self, f"_{attachment}_options")
        if options['required'] and not getattr(self, attachment):
            self.errors.append(f'{attachment} should not be blank.')

def attachment_folder(self, options, full_path=True):
    if full_path:
        return os.path.join(os.environ["ROOT_PROJECT_PATH"], 'public', 'attachments', options['bucket'])
    else:
        return '/' + os.path.join('attachments', options['bucket'])

def delete_file(self, file_name, options):
    file_path = os.path.join(self.attachment_folder(options), file_name)
    try:
        os.remove(file_path)
        print(f"'{file_path}' has been successfully deleted.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_field_method(cls, field_name):
    def field_url(self):
        file_name = getattr(self, field_name)
        if file_name:
            folder_path = self.attachment_folder(getattr(self, f"_{field_name}_options"), full_path=False)
            return os.path.join(folder_path, file_name)
        else:
            return ""
    
    method = types.FunctionType(
        field_url.__code__,
        globals(),
        f'{field_name}_url',
        closure=(field_url.__closure__[0],),
    )
    setattr(cls, f'{field_name}_url', method)