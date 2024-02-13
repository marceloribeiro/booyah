### The Booyah ORM

Booyah ORM will provide a series of methods and features to make it easy to query your database and return the records you need.

To get started, try it out using your console:

```
booyah c
```

**Create, Update, Delete**

You can start creating a new record easily with one of the methods below:

```
blog = Blog.create({"title": "Something nice", "description": "A longer description", "published": False})
```

**Fetching Records**

You can start by fetching al records form the table:

```
blogs = Blog.all()
for blog in blogs:
	print(blog.title)

```

Or find a single record by the primary key:

```
blog = Blog.find(1)
```

Update an existing record:

```
blog.update({"published": True})
```

You can also set each attribute individually and call `save` at any time:

```
blog.published = False
blog.save()
```

Lastly, if you want to delete a record:


```
blog.destroy()
```

**Querying**

Querying works using the `where` call:

```
published_blogs = Blog.where("is_published = ?", True)
published_blogs.first().title
```

The querying object also allows for chained querying:

```
published_blogs_since_yesterday = Blog.where("is_published = ?", True).where("created_at >= ?", "2023-09-17 00:00:00")
published_blogs_since_yesterday.count()
1
```

Some other elements available to the querying object:

```
blogs = Blog.select('title')
blogs = blogs.order('title ASC')
blogs = blogs.join('users', 'blogs.user_id = users.id')
```

Counting elements from a query:

```
blogs.count()
1
```
