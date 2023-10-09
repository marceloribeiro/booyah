import types
import boto3
from botocore.exceptions import NoCredentialsError
import os
from booyah.models.helpers.attachment_helper import _save_attachments, _validate_attachments, _attachment_folder, _delete_file, _add_field_method, _delete_all_files
from booyah.observers.application_model_observer import ApplicationModelObserver

class Attachment:
    @staticmethod
    def configure(cls, name, required=False, bucket="booyah", content_types=[]):
        if not hasattr(cls, '_attachments'):
            cls._attachments = [name]
        else:
            cls._attachments.append(name)
        setattr(cls, f"_{name}_options", {
            'required': required,
            'bucket': bucket,
            'content_types': content_types
        })
        Attachment.copy_required_methods_to_class(cls)
        Attachment.add_methods(cls, name)
        if not hasattr(cls, 'custom_validates'):
            cls.custom_validates = []
        cls.custom_validates.append(cls._validate_attachments)
        ApplicationModelObserver.add_callback('before_save', cls.__name__, '_save_attachments')
        ApplicationModelObserver.add_callback('after_destroy', cls.__name__, '_delete_all_files')

    @staticmethod
    def copy_required_methods_to_class(cls):
        cls._validate_attachments = _validate_attachments
        cls._save_attachments = _save_attachments
        cls._save_local_attachment = Attachment._save_local_attachment.__get__(cls)
        cls._delete_file = _delete_file
        cls._delete_all_files = _delete_all_files
        cls._attachment_folder = _attachment_folder

    def _save_local_attachment(self, source_path, destination_path):
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        os.rename(source_path, destination_path)
    
    @staticmethod
    def add_methods(cls, name):
        _add_field_method(cls, name)