**Running Booyah From Project Folder**

If you want to run booyah from source folder, you should enter the src folder and run:

```sh
$ python -m booyah --version
```

**Attachments**

Before using attachments, you must to run the install and migrate commands:
```sh
$ booyah g attachments install
$ booyah db migrate
```

You can automatically create and configure attachment field by using scaffold field type file, example:
```sh
$ booyah g scaffold User name:string photo:file
```
or
You can configure an attachment file to a model by adding folowing code:

> from booyah.models.booyah_attachment import BooyahAttachment
>
> class User(ApplicationModel):
>  pass
> BooyahAttachment.configure(User, 'photo', required=True, bucket='photos')

You can also configure multiple attachments using multiple storage types:

> class User(ApplicationModel):
>     pass
> BooyahAttachment.configure(User, 'photo', bucket='booyahtest', \
>     file_extensions=['.png', '.jpg', '.jpeg', '.ico', '.gif', '.bmp'], \
>     storage={'type': 's3', 'ACCESS_KEY': os.environ.get('AWS_ACCESS_KEY_ID'), \
>     'SECRET_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'), 'SESSION_TOKEN': None})
> BooyahAttachment.configure(User, 'document', bucket='booyahtest', \
>     file_extensions=['.doc', '.rtf', '.docx', '.pdf', '.txt'])

This will configure photo string field to work as an attachment, you can create an html input field user[photo] and it will be uploaded as a booyah File.

You can also create a global config, it will be used as default for all attachments that is not changing the config, for that, configure the following vars:

> # Attachment Global Config
> BOOYAH_ATTACHMENT_REQUIRED=False
> BOOYAH_ATTACHMENT_BUCKET=bucket_name
> BOOYAH_ATTACHMENT_EXTENSIONS=jpg,png,doc,docx,pdf
> BOOYAH_ATTACHMENT_SIZE='{"min": 0, "max": 52428800}'
> BOOYAH_ATTACHMENT_STORAGE='{
>     "type": "s3",
>     "ACCESS_KEY": "...",
>     "SECRET_KEY": "...",
>     "SESSION_TOKEN": "",
> }'

**Logging**

Check for configurations in .env file, you can change LOG_LEVEL and LOG_FILE_PATH.

Usage:

> from lib.logger import logger
> ...
> logger.debug('Debug message', debug_object1, 'other message', debug_object2, ...)
> logger.info('Debug message', debug_object, delimiter=', ')

**Inflections**

You can easily use inflections by using a String class.

Examples:

>>> a = String('Hello World')
>>> a.pluralize()
'Hello Worlds'
>>> a.pluralize().underscore()
'Hello_Worlds'
>>> a.pluralize().underscore().singularize()
'Hello_World'
>>> a.pluralize().underscore().singularize().classify()
'HelloWorld'
>>> a.pluralize().underscore().singularize().classify().pluralize()
'HelloWorlds'
>>> (String('Hello') + 'World').pluralize()
'HelloWorlds'
>>> ('Hello' + String('World')).pluralize()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'str' object has no attribute 'pluralize'