![alt TestRunner](https://github.com/marceloribeiro/booyah/actions/workflows/tests_runner.yml/badge.svg)

## Booyah Framework

Booyah is a MVC web framework written in Python that aims to be easy to use while setting up projects quickly. It follows the convention over configuration paradigm introduced by Ruby on Rails.

The following links detail the process of installing and setting up your first project.


[1. Installation](docs/install.md)

[2. Getting Started](docs/getting-started.md)

### 4. The Booyah Console

Booyah comes in with a preconfigured console you can use to access your models and other classes within the framework:

```
booyah c

>>> blog = Blog()
>>> blog.title = 'Something'
>>> blog.description = 'Else'
>>> blog.save()
>>> blog.to_dict()
{'created_at': '2023-09-17 20:11:55.260098', 'description': 'Else', 'id': 2, 'is_published': None, 'title': 'Something', 'updated_at': '2023-09-17 20:11:55.260129'}
>>> blog.update({"is_published": True})
```

### 5. Booyah ORM Querying

Booyah ORM will provide a series of methods and features to make it easy to query your database and return the elements you need:

```
booyah c

>>> blogs = Blog.all()
>>> for blog in blogs:
>>> 	print(blog.title)


>>> blog = Blog.find(1)

>>> published_blogs = Blog.where("is_published = ?", True)
>>> published_blogs.first().title
```

And the ORM querying object also allows for chained querying:

```
>>> published_blogs_since_yesterday = Blog.where("is_published = ?", True).where("created_at >= ?", "2023-09-17 00:00:00")
published_blogs_since_yesterday.count()
1
```

Some other elements available to the querying object:

```
>>> blogs = Blog.select('title')
>>> blogs = blogs.order('title ASC')
>>> blogs = blogs.join('users', 'blogs.user_id = users.id')
>>> blogs.count()
1
```

### 6. Controllers and Actions

Booyah controllers are classes defined by <CONTROLLER_NAME>Controller, and methods that work as actions, mapped via the routes file.

We also implemented support for before, after and around action blocks:

```
class BlogsController:
	before_action('authenticate_user')

	def index:
		# render the blog posts

	def authenticate_user:
		# make sure the user is authenticated or return the error
```

`before_action`, `after_action` and `around_action` calls also support configurations for specific actions:

```
class CartsController:
	before_action('authenticate_user', only_for=['checkout']

	def create:
		# creates a new shopping cart

	def checkout:
		# checks out the cart to become a new order
```

Or you can also skip before_action that has been setup on a parent controller class (like ApplicationController for example)

```
class CartsController:
	skip_before_action('authenticate_user', except_for=['checkout']

	def create:
		# creates a new shopping cart

	def checkout:
		# checks out the cart to become a new order
```

### 7. Collaborating

You can collaborate with Booyah by forking the repo and submitting a pull request. We are very early stage so any help is welcome. We do try to follow the Rails way in Python though, so please keep that in mind.