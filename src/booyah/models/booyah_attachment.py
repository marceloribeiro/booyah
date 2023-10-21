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
    after_destroy('delete_file')

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
    
    def record_options(self):
        self.import_model(self.record_type, globals())
        return getattr(globals()[self.record_type], f"_{self.name}_options")

    def url(self, loaded_record=None):
        r = loaded_record if loaded_record else self.record()
        return BooyahAttachment.field_url(r, self.name, self.key)
    
    def insert(self, validate=True):
        self.record_id = self.record_id if self.record_id else self.record.id
        if validate and not self.valid():
            return False
        self.save_file()
        if not super().insert(validate=False):
            self.delete_file()
    
    def update(self, attributes = None, validate=True):
        self.record_id = self.record_id if self.record_id else self.record.id
        if validate and not self.valid():
            return False
        self.save_file()
        if not super().update(attributes, validate=False):
            self.delete_file()

    def save_file(self):
        if not self.file_object:
            return

        if type(self.file_object) is File:
            if self.key:
                self.storage().delete_file(self.key)
            new_file_name = BooyahAttachment.storage_for(self.record, self.name).save(self.file_object)
            if new_file_name:
                self.key = new_file_name
                self.filename = self.file_object.original_file_name
                self.extension = str(self.file_object).split('.')[-1]
                self.byte_size = self.file_object.file_length

    def delete_file(self):
        self.storage().delete_file(self.key)
        setattr(self.record, self.name, None)
    
    @staticmethod
    def find_attachment(record, field_name):
        return BooyahAttachment.where('record_id', record.id) \
                .where('record_type', record.__class__.__name__) \
                .where('name', field_name).first()
    
    @staticmethod
    def configure(klass, name, required=False, bucket="booyah", file_extensions=['*'], \
                    size={'min': 0, 'max': Number(50).megabytes()}, \
                    storage={'type': 'local'}):
        if not hasattr(klass, '_attachments'):
            klass._attachments = [name]
        else:
            klass._attachments.append(name)
        setattr(klass, f"_{name}_options", {
            'required': required,
            'bucket': bucket,
            'file_extensions': file_extensions,
            'size': size,
            'storage': storage
        })
        BooyahAttachment.copy_required_methods_to_class(klass)
        _add_field_methods(klass, name)
        klass._has_one.append({
            'name': name,
            'dependent': 'destroy',
            'class_name': BooyahAttachment.__name__,
            'foreign_key': 'record_id'
        })

    @staticmethod
    def copy_required_methods_to_class(cls):
        cls._validate_attachments = _validate_attachments
        cls._s3_instance = _s3_instance
        cls._attachment_url = _attachment_url

    @staticmethod
    def field_url(record, field_name, file_name):
        return BooyahAttachment.storage_for(record, field_name).url(file_name)

    def storage(self):
        options = getattr(self.record.__class__, f"_{self.name}_options")
        if options['storage']['type'] == 's3':
            return S3Storage(self.record, self.name, options)
        else:
            return LocalStorage(self.record, self.name, options)

    @staticmethod
    def storage_for(record, field_name):
        options = getattr(record, f"_{field_name}_options")
        if options['storage']['type'] == 's3':
            return S3Storage(record, field_name, options)
        else:
            return LocalStorage(record, field_name, options)

    def file_validation(self):
        options = getattr(self.record, f"_{self.name}_options")
        current_value = self.file_object
        if options['required'] and not current_value:
            self.errors.append(f"{self.name} file should not be blank.")
        if type(current_value) is File:
            if options['file_extensions'] and '*' not in options['file_extensions']:
                root, extension = os.path.splitext(current_value.file_path)
                if extension not in options['file_extensions']:
                    error_message = f"{self.name} '{current_value.original_file_name}' is not a valid file type ({','.join(options['file_extensions'])})."
                    self.errors.append(error_message)
            if options['size'] and options['size']['min'] and current_value.file_length < options['size']['min']:
                self.errors.append(f"{self.name} should have at least {options['size']['min']} bytes.")
            if options['size'] and options['size']['max'] and current_value.file_length > options['size']['max']:
                    self.errors.append(f"{self.name} should have at most {options['size']['max']} bytes.")

BooyahAttachment._custom_validates.append(BooyahAttachment.file_validation)

def _validate_attachments(self):
    BooyahAttachment.validate_model_attachments(self)

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
            booyah_attachment = None
            if getattr(self, field_name):
                booyah_attachment = getattr(self, field_name)
                booyah_attachment.file_object = value
            else:
                booyah_attachment = BooyahAttachment({
                    'file_object': value,
                    'name': field_name,
                })
            booyah_attachment.record = self
            setattr(self, private_name, booyah_attachment)
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