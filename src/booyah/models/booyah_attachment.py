from booyah.models.application_model import ApplicationModel
from booyah.models.helpers.local_storage import LocalStorage
from booyah.models.helpers.s3_storage import S3Storage
from booyah.models.file import File
from booyah.observers.application_model_observer import ApplicationModelObserver
import types
import boto3
from botocore.exceptions import NoCredentialsError
import os
from booyah.extensions.number import Number
from booyah.models.helpers.callbacks import after_destroy

class BooyahAttachment(ApplicationModel):
    after_destroy('custom_destroy')

    def __init__(self, attributes={}):
        super().__init__(attributes)
        self.file_object = attributes.get('file_object')

    @property
    def record(self):
        if not hasattr(self, '__record') and self.record_type and self.record_id:
            self.import_model(self.record_type, globals())
            self.__record = globals()[self.record_type].find(self.record_id)
        return self.__record

    @record.setter
    def record(self, new_value):
        self.__record = new_value
        if new_value:
            self.record_type = new_value.__class__.__name__
            self.record_id = new_value.id
    
    def custom_destroy(self):
        breakpoint()
        print('it comes custom_destroy')
    
    def record_options(self):
        self.import_model(self.record_type, globals())
        return getattr(globals()[self.record_type], f"_{self.name}_options")

    def url(self, loaded_record=None):
        r = loaded_record if loaded_record else self.record()
        return BooyahAttachment.field_url(r, self.name, self.key)
    
    def save(self):
        for field_name in record._attachments:
            options = getattr(record, f"_{field_name}_options")
            current_value = getattr(record, field_name)
            should_delete = getattr(record, f'_destroy_{field_name}')
            previous_value = None if not hasattr(record, f"{field_name}_was") else getattr(record, f"{field_name}_was")
            if should_delete and type(previous_value) is not File:
                BooyahAttachment.delete_model_attachment(record, field_name)
                continue
            if type(previous_value) is File:
                previous_value = None
            if type(current_value) is File:
                if previous_value:
                    BooyahAttachment.delete_model_attachment(record, field_name)
                BooyahAttachment.save_model_attachment(record, field_name, current_value)
    
    @staticmethod
    def find_attachment(record, field_name):
        return BooyahAttachment.where('record_id', record.id) \
                .where('record_type', record.__class__.__name__) \
                .where('name', field_name).first()
    
    @staticmethod
    def configure(cls, name, required=False, bucket="booyah", file_extensions=['*'], \
                    size={'min': 0, 'max': Number(50).megabytes()}, \
                    storage={'type': 'local'}):
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
        BooyahAttachment.copy_required_methods_to_class(cls)
        _add_field_methods(cls, name)
        if not hasattr(cls, 'custom_validates'):
            cls.custom_validates = []
        
        if not cls._validate_attachments in cls.custom_validates:
            cls.custom_validates.append(cls._validate_attachments)
        cls._has_one.append(name)
        cls.accessors.append(f'_destroy_{name}')
        # ApplicationModelObserver.add_callback('after_save', cls.__name__, '_save_attachments')
        ApplicationModelObserver.add_callback('after_destroy', cls.__name__, '_delete_all_files')

    @staticmethod
    def copy_required_methods_to_class(cls):
        cls._validate_attachments = _validate_attachments
        cls._save_attachments = _save_attachments
        cls._delete_all_files = _delete_all_files
        cls._s3_instance = _s3_instance
        cls._attachment_url = _attachment_url
    
    @staticmethod
    def save_model_attachment(record, field_name, file_value):
        new_file_name = BooyahAttachment.storage_for(record, field_name).save(file_value)
        BooyahAttachment.create({
            'record_id': record.id,
            'record_type': record.__class__.__name__,
            'name': field_name,
            'key': new_file_name,
            'filename': file_value.original_file_name,
            'extension': str(file_value).split('.')[-1],
            'byte_size': file_value.file_length,
        })
        setattr(record, field_name, file_value.original_file_name)

    # @staticmethod
    # def save_model_attachments(record):
    #     for field_name in record._attachments:
    #         options = getattr(record, f"_{field_name}_options")
    #         current_value = getattr(record, field_name)
    #         should_delete = getattr(record, f'_destroy_{field_name}')
    #         previous_value = None if not hasattr(record, f"{field_name}_was") else getattr(record, f"{field_name}_was")
    #         if should_delete and type(previous_value) is not File:
    #             BooyahAttachment.delete_model_attachment(record, field_name)
    #             continue
    #         if type(previous_value) is File:
    #             previous_value = None
    #         if type(current_value) is File:
    #             if previous_value:
    #                 BooyahAttachment.delete_model_attachment(record, field_name)
    #             BooyahAttachment.save_model_attachment(record, field_name, current_value)

    @staticmethod
    def field_url(record, field_name, file_name):
        return BooyahAttachment.storage_for(record, field_name).url(file_name)

    @staticmethod
    def field_value(record, field_name):
        pass

    @staticmethod
    def delete_model_attachment(record, field_name, file_name=None):
        query = BooyahAttachment.where('record_id', record.id) \
                .where('record_type', record.__class__.__name__) \
                .where('name', field_name)
        if file_name:
            query = query.where('filename', file_name)
        query.destroy_all()
        query.cleanup()
        setattr(record, field_name, None)

    @staticmethod
    def delete_model_attachments(record):
        for field_name in record._attachments:
            BooyahAttachment.delete_model_attachment(record, field_name)

    @staticmethod
    def storage_for(record, field_name):
        options = getattr(record, f"_{field_name}_options")
        if options['storage']['type'] == 's3':
            return S3Storage(record, field_name, options)
        else:
            return LocalStorage(record, field_name, options)

    @staticmethod
    def validate_model_attachments(record):
        for field_name in record._attachments:
            options = getattr(record, f"_{field_name}_options")
            current_value = getattr(record, field_name)
            if options['required'] and not current_value:
                record.errors.append(f"{field_name} should not be blank.")
            if type(current_value) is File:
                if options['file_extensions'] and '*' not in options['file_extensions']:
                    root, extension = os.path.splitext(current_value.file_path)
                    if extension not in options['file_extensions']:
                        error_message = f"{field_name} '{current_value.original_file_name}' is not a valid file type ({','.join(options['file_extensions'])})."
                        record.errors.append(error_message)
                if options['size'] and options['size']['min'] and current_value.file_length < options['size']['min']:
                    record.errors.append(f"{field_name} should have at least {options['size']['min']} bytes.")
                if options['size'] and options['size']['max'] and current_value.file_length > options['size']['max']:
                    record.errors.append(f"{field_name} should have at most {options['size']['max']} bytes.")


def _validate_attachments(self):
    BooyahAttachment.validate_model_attachments(self)

#def _save_attachments(self):
#    BooyahAttachment.save_model_attachments(self)

def _delete_all_files(self):
    BooyahAttachment.delete_model_attachments(self)

def _s3_instance(self, field_name):
    if not hasattr(self, f"_{field_name}_options"):
        raise ValueError(f'the attribute {self.__class__.__name__}.{field_name} is not an attachment field!')
    options = getattr(self, f"_{field_name}_options")
    if options['storage']['type'] != 's3':
        raise ValueError(f'the attribute {self.__class__.__name__}.{field_name} is not configured to use s3 storage!')
    s3_attribute = f'_s3_{field_name}'
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
            raise ValueError(f"s3 bucket for {self.__class__.__name__}.{field_name} named {options['bucket']} not found!")
    return getattr(self, s3_attribute)

def _attachment_url(self, attachment, file_name):
    return BooyahAttachment.field_url(self, attachment, file_name)

def _add_field_methods(cls, field_name):
    private_name = f'__{field_name}'
    
    def get_attachment(self):
        if not hasattr(self, private_name) or getattr(self, private_name) == None:
            result = BooyahAttachment.where('record_id', self.id) \
                .where('record_type', self.__class__.__name__) \
                .where('name', field_name).first()
            setattr(self, private_name, result)
        return getattr(self, private_name)

    def set_attachment(self, value):
        if value is not None and not isinstance(value, File) and not isinstance(value, BooyahAttachment):
            raise ValueError(f"{self.__class__.__name__}.{field_name} must be a File or BooyahAttachment")
        if isinstance(value, File):
            new_booyah_attachment = BooyahAttachment({
                'file_object': value,
                'name': field_name,
            })
            new_booyah_attachment.record = self
            setattr(self, private_name, new_booyah_attachment)
        else:
            setattr(self, private_name, value)

    setattr(cls, field_name, property(get_attachment, set_attachment))

    def field_url(self):
        booyah_attachment = getattr(self, field_name)
        if booyah_attachment:
            return booyah_attachment.url(loaded_record=self)
        else:
            return ""
    
    method1 = types.FunctionType(
        field_url.__code__,
        globals(),
        f'{field_name}_url',
        closure=(field_url.__closure__[0],),
    )
    setattr(cls, f'{field_name}_url', method1)