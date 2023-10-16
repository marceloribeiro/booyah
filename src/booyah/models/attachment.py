import types
import boto3
from botocore.exceptions import NoCredentialsError
import os
from booyah.models.helpers.attachment_helper import _save_attachments, _validate_attachments, \
    _attachment_folder, _delete_file, _add_field_method, _delete_all_files, _s3_instance, \
    _storage_for, _save_attachment, _attachment_url
from booyah.observers.application_model_observer import ApplicationModelObserver
from booyah.extensions.number import Number

class Attachment:

    @staticmethod
    def configure(cls, name, required=False, bucket="booyah", file_extensions=['*'], size={'min': 0, 'max': Number(50).megabytes()}, storage={'type': 'local'}):
        if not hasattr(cls, '_attachments'):
            cls._attachments = [name]
        else:
            cls._attachments.append(name)
        setattr(cls, f"_{name}_options", {
            'required': required,
            'bucket': bucket,
            'file_extensions': file_extensions,
            'size': size,
            'storage': storage
        })
        Attachment.copy_required_methods_to_class(cls)
        Attachment.add_methods(cls, name)
        if not hasattr(cls, 'custom_validates'):
            cls.custom_validates = []
        cls.custom_validates.append(cls._validate_attachments)
        cls.accessors.append(f'_destroy_{name}')
        ApplicationModelObserver.add_callback('before_save', cls.__name__, '_save_attachments')
        ApplicationModelObserver.add_callback('after_destroy', cls.__name__, '_delete_all_files')

    @staticmethod
    def copy_required_methods_to_class(cls):
        cls._validate_attachments = _validate_attachments
        cls._save_attachments = _save_attachments
        cls._save_attachment = _save_attachment
        cls._delete_file = _delete_file
        cls._delete_all_files = _delete_all_files
        cls._attachment_folder = _attachment_folder
        cls._s3_instance = _s3_instance
        cls._storage_for = _storage_for
        cls._attachment_url = _attachment_url
    
    @staticmethod
    def add_methods(cls, name):
        _add_field_method(cls, name)