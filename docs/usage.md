**Generators**

You can easily generate a controller file with given actions using command line:

```sh
$ booyah generate controller HelloWorld action1 action2
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