### Booyah Generators

Booyah comes with some built-in generators that should facilitate the process of building a project. 

**1. Project Generator**

You can use the project generator to start a new booyah project fairly simply:

```
booyah new <PROJECT_NAME>
```

Example:

```
Booyah new blog
```

**2. Scaffold Generator**

A scaffold is a combination of the following components for a fully featured REST experience: a model, a migration, a controller, the views, and a route.

You can start by generating a sample scaffold to learn how it works:

```
booyah g scaffold <ENTITY_NAME> <ATTRIBUTES:ATTRIBUTE_TYPES>
```

Example:

```
booyah g scaffold blog_post title:string content:text published:boolean view_count:integer published_at:datetime
```

**3. Controller generator**

You can go simple by generating just a controller using the following:


```
booyah g controller <CONTROLLER_NAME> <CONTROLLER_ACTIONS>
```

Example:

```
booyah g controller home index about contact
```