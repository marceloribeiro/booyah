import os
from booyah.models.file import File
import uuid
import types
import boto3

def _s3_instance(self, attachment, options):
    s3_attribute = f'_s3_{attachment}'
    if not hasattr(self, ):
        session = boto3.Session(
            aws_access_key_id=options['storage']['ACCESS_KEY'],
            aws_secret_access_key=options['storage']['SECRET_KEY'],
            aws_session_token=options['storage']['SESSION_TOKEN'],
        )

        setattr(self, s3_attribute, session.resource('s3'))
    return getattr(self, s3_attribute)

def _save_attachments(self):
    for attachment in self._attachments:
        options = getattr(self, f"_{attachment}_options")
        current_value = getattr(self, attachment)
        should_delete = getattr(self, f'_destroy_{attachment}')
        previous_value = None if not hasattr(self, f"{attachment}_was") else getattr(self, f"{attachment}_was")
        if should_delete and type(previous_value) is not File:
            self._delete_file(previous_value, options)
            setattr(self, attachment, None)
            continue
        if type(previous_value) is File:
            previous_value = None
        if type(current_value) is File:
            if previous_value:
                self._delete_file(previous_value, options)
            random_filename = str(uuid.uuid4())
            extension = str(current_value).split('.')[-1]
            full_file_name = f"{random_filename}.{extension}"

            if os.getenv('BOOYAH_ENV') != 'production':
                target_path = os.path.join(self._attachment_folder(options), full_file_name)
                self._save_local_attachment(str(current_value), target_path)
                setattr(self, attachment, full_file_name)

def _validate_attachments(self):
    for attachment in self._attachments:
        options = getattr(self, f"_{attachment}_options")
        current_value = getattr(self, attachment)
        if options['required'] and not current_value:
            self.errors.append(f"{attachment} should not be blank.")
        if type(current_value) is File:
            if options['file_extensions'] and '*' not in options['file_extensions']:
                root, extension = os.path.splitext(current_value.file_path)
                if extension not in options['file_extensions']:
                    error_message = f"{attachment} '{current_value.original_file_name}' is not a valid file type ({','.join(options['file_extensions'])})."
                    self.errors.append(error_message)
            if options['size'] and options['size']['min'] and current_value.file_length < options['size']['min']:
                self.errors.append(f"{attachment} should have at least {options['size']['min']} bytes.")
            if options['size'] and options['size']['max'] and current_value.file_length > options['size']['max']:
                self.errors.append(f"{attachment} should have at most {options['size']['max']} bytes.")


def _attachment_folder(self, options, full_path=True):
    if full_path:
        return os.path.join(os.environ["ROOT_PROJECT_PATH"], 'public', 'attachments', options['bucket'])
    else:
        return '/' + os.path.join('attachments', options['bucket'])

def _delete_file(self, file_name, options):
    file_path = os.path.join(self._attachment_folder(options), file_name)
    try:
        os.remove(file_path)
        print(f"'{file_path}' has been successfully deleted.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def _delete_all_files(self):
    for attachment in self._attachments:
        options = getattr(self, f"_{attachment}_options")
        current_value = getattr(self, attachment)
        self._delete_file(current_value, options)

def _add_field_method(cls, field_name):
    def field_url(self):
        file_name = getattr(self, field_name)
        if file_name:
            folder_path = self._attachment_folder(getattr(self, f"_{field_name}_options"), full_path=False)
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