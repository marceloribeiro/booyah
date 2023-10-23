
**Create a new Booyah project**

To start a new booyah project run the 'new' command followed by the project name, it will create a project folder in the current directory.

```sh
$ booyah new ProjectName
```

**Configure**

You can use you custom settings for the project by changing the .env file in the root project folder

**Generators**

You can start by using a scaffold generator that will create table migration, model, controller and views:

```sh
$ booyah generate scaffold user name:string
```

Note: Don't forget to run the migration command

You can easily generate a controller file with given actions using command line:

```sh
$ booyah generate controller HelloWorld action1 action2
```

or just

```sh
$ booyah g controller HelloWorld action1 action2
```

**Database Operations**

You can easily execute some database operations as following:

```sh
$ booyah db create
$ booyah db migrate
$ booyah db rollback
$ booyah db seed
$ booyah db drop

$ VERSION=20230911982982 booyah db migrate
$ VERSION=20230911982982 booyah db migrate_up
$ VERSION=20230911982982 booyah db migrate_down

or

$ booyah db migrate 20230911982982
$ booyah db migrate_up 20230911982982
$ booyah db migrate_down 20230911982982

```

You can also connect to project database with the following command:

```sh
$ booyah db
```

**Console**

You can start booyah console to test models, inflections, it is a python console with booyah framework loaded.

```sh
$ booyah c
```

**Start Server**

To start booyah server, running with gunicorn http server, just run in the project folder following command:

```sh
$ booyah s
```

**Running Booyah From Project Folder**

If you want to run booyah from source folder, you should enter the src folder and run:

```sh
$ python -m booyah --version
```

**Attachments**

Before using attachments, you have to run the install command, and migrate command, it will create required table:
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

> from booyah.models.attachment import Attachment
> 
> class User(ApplicationModel):
>  pass
> Attachment.configure(User, 'photo', required=True, bucket='photos')

You can also configure multiple attachments using multiple storage types:

> class User(ApplicationModel):
>     pass
> Attachment.configure(User, 'photo', bucket='booyahtest', \
>     file_extensions=['.png', '.jpg', '.jpeg', '.ico', '.gif', '.bmp'], \
>     storage={'type': 's3', 'ACCESS_KEY': os.environ.get('AWS_ACCESS_KEY_ID'), \
>     'SECRET_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'), 'SESSION_TOKEN': None})
> Attachment.configure(User, 'document', bucket='booyahtest', \
>     file_extensions=['.doc', '.rtf', '.docx', '.pdf', '.txt'])

This will configure photo string field to work as an attachment, you can create an html input field user[photo] and it will be uploaded as a booyah File.

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