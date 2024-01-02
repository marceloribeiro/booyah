### The Booyah Console

Booyah comes in with a preconfigured console you can use to access your models and other classes within the framework:

To access the console, run the following from the terminal, inside the project folder:

```
booyah c
```

Models are available from the console, and automatically imported:

```
>>> blog = Blog()
>>> blog.title = 'Something'
>>> blog.description = 'Else'
>>> blog.save()
>>> blog.to_dict()
{'created_at': '2023-09-17 20:11:55.260098', 'description': 'Else', 'id': 2, 'is_published': None, 'title': 'Something', 'updated_at': '2023-09-17 20:11:55.260129'}
>>> blog.update({"is_published": True})
```
