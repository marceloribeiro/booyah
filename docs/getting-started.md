
### Getting Started with Booyah

Welcome to Booyah! This guide will walk you through creating and setting up your first Booyah project.

#### Step 1: Create Your Project

To start, generate a new project with the following command:

```bash
booyah new YOUR_PROJECT_NAME
```

This command creates several files, including `config/application.yml`, which contains essential settings such as database connection information. **Important:** Update `config/application.yml` with your database name, replacing the default if necessary.

#### Step 2: Set Up Your Database

Booyah currently supports PostgreSQL databases. To set up your first database, navigate to your project directory and run:

```bash
booyah db create
booyah db migrate
```

This process initializes and migrates your database.

#### Step 3: Run the Server

With your database ready, start the Booyah server:

```bash
booyah s
```

You can then access your project at http://localhost:8000. The `routes.py` file contains sample routes for your reference.

#### Step 4: Create RESTful Resources

Booyah follows RESTful resource patterns. To generate a resource, use the scaffold generator:

```bash
booyah g scaffold blog title description:text is_published:boolean
```

Executing this command will create:

- A database migration for the blog table.
- A `Blog` model.
- A `Blog` serializer for JSON APIs.
- A `Blogs` controller with CRUD actions.
- Routes for blog resources.
- HTML views for the blog.

#### Step 5: Migrate the Database Again

After generating your resource, run another migration to set up the necessary table:

```bash
booyah db migrate
```

#### Step 6: Explore Your New Resource

Visit https://localhost:8000/blogs to manage blog posts. The `routes.py` file is updated with endpoints for your blog resources.

---

By following these steps, you'll have a functional Booyah project ready for development. Happy coding!
