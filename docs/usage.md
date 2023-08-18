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
