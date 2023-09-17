import os
from booyah.models.file import File
import uuid

def save_attachments(self, attributes = None):
    if not attributes:
        return attributes

    for attachment in self._attachments:
        if attachment not in attributes.keys():
            continue
        options = getattr(self, f"_{attachment}_options")
        current_value = attributes[attachment]
        previous_value = None if not hasattr(self, f"{attachment}_was") else getattr(self, f"{attachment}_was")
        if type(current_value) is File:
            if previous_value:
                self.delete_file(previous_value, options)
            random_filename = str(uuid.uuid4())
            extension = str(current_value).split('.')[-1]
            full_file_name = f"{random_filename}.{extension}"

            if os.getenv('BOOYAH_ENV') != 'production':
                target_path = os.path.join(self.attachment_folder(options), full_file_name)
                self.save_local_attachment(str(current_value), target_path)
                attributes[attachment] = full_file_name
                setattr(self, attachment, full_file_name)
        elif current_value == None and previous_value:
            self.delete_file(previous_value, options)
    return attributes

def validate_attachments(self):
    for attachment in self._attachments:
        options = getattr(self, f"_{attachment}_options")
        if options['required'] and not getattr(self, attachment):
            self.errors.append(f'{attachment} should not be blank.')

def attachment_folder(self, options):
    return os.path.join(os.environ["ROOT_PROJECT_PATH"], 'public', 'attachments', options['bucket'])

def delete_file(self, file_name, options):
    file_path = os.path.join(self.attachment_folder(options), file_name)
    try:
        os.remove(file_path)
        print(f"'{file_path}' has been successfully deleted.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")