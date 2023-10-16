import os
from booyah.models.file import File
from booyah.models.helpers.local_storage import LocalStorage
from booyah.models.helpers.s3_storage import S3Storage
import types
import boto3

def _s3_instance(self, attachment):
    if not hasattr(self, f"_{attachment}_options"):
        raise ValueError(f'the attribute {self.__class__.__name__}.{attachment} is not an attachment field!')
    options = getattr(self, f"_{attachment}_options")
    if options['storage']['type'] != 's3':
        raise ValueError(f'the attribute {self.__class__.__name__}.{attachment} is not configured to use s3 storage!')
    s3_attribute = f'_s3_{attachment}'
    if not hasattr(self, s3_attribute):
        session = boto3.Session(
            aws_access_key_id=options['storage']['ACCESS_KEY'],
            aws_secret_access_key=options['storage']['SECRET_KEY'],
            aws_session_token=options['storage']['SESSION_TOKEN'],
        )

        setattr(self, s3_attribute, session.resource('s3'))
        found_bucket = False
        for bucket in session.resource('s3').buckets.all():
            if bucket.name == options['bucket']:
                found_bucket = True
        if not found_bucket:
            raise ValueError(f"s3 bucket for {self.__class__.__name__}.{attachment} named {options['bucket']} not found!")
    return getattr(self, s3_attribute)

def _save_attachments(self):
    for attachment in self._attachments:
        options = getattr(self, f"_{attachment}_options")
        current_value = getattr(self, attachment)
        should_delete = getattr(self, f'_destroy_{attachment}')
        previous_value = None if not hasattr(self, f"{attachment}_was") else getattr(self, f"{attachment}_was")
        if should_delete and type(previous_value) is not File:
            self._delete_file(attachment, previous_value)
            setattr(self, attachment, None)
            continue
        if type(previous_value) is File:
            previous_value = None
        if type(current_value) is File:
            if previous_value:
                self._delete_file(attachment, previous_value)
            setattr(self, attachment, self._save_attachment(attachment, current_value))

def _save_attachment(self, attachment, file_value):
    return self._storage_for(attachment).save(file_value)

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


def _attachment_folder(self, attachment, full_path=True):
    return self._storage_for(attachment).attachment_folder(full_path)

def _attachment_url(self, attachment, file_name):
    return self._storage_for(attachment).url(file_name)

def _storage_for(self, attachment):
    options = getattr(self, f"_{attachment}_options")
    if options['storage']['type'] == 's3':
        return S3Storage(self, attachment, options)
    else:
        return LocalStorage(self, attachment, options)

def _delete_file(self, attachment, file_name):
    return self._storage_for(attachment).delete_file(file_name)

def _delete_all_files(self):
    for attachment in self._attachments:
        options = getattr(self, f"_{attachment}_options")
        current_value = getattr(self, attachment)
        if current_value:
            self._delete_file(attachment, current_value)

def _add_field_method(cls, field_name):
    def field_url(self):
        file_name = getattr(self, field_name)
        if file_name:
            return self._attachment_url(field_name, file_name)
        else:
            return ""
    
    method = types.FunctionType(
        field_url.__code__,
        globals(),
        f'{field_name}_url',
        closure=(field_url.__closure__[0],),
    )
    setattr(cls, f'{field_name}_url', method)