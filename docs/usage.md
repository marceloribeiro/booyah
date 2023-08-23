**Generators**

You can easily generate a controller file with given actions using command line:

```sh
$ booyah generate controller HelloWorld action1 action2
```

or just

```sh
$ booyah g controller HelloWorld action1 action2
```

**Create a new Booyah project**

To start a new booyah project run the 'new' command followed by the project name, it will create a project folder in the current directory.

```sh
$ booyah new ProjectName
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