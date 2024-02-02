### Database Operations

Booyah was designed to also make it easy to manage your database, from migrations to console access. Here are some shortcuts you can take advantage from:

* Creates the booyah database defined in config/application.yml
```sh
$ booyah db create
```

* Runs the new/pending database migrations
```sh
$ booyah db migrate
```

* Rolls back the last database migration

```sh
$ booyah db rollback
```

* Sseeds the data defined in seeds.py

```sh
$ booyah db seed
```

* Drops/removes the database defined in config/application.yml

```sh
$ booyah db drop
```

* Migrates to a specific version

```sh
$ VERSION=20230911982982 booyah db migrate
# or
$ booyah db migrate 20230911982982
```

* Migrate up a specific version

```sh
$ VERSION=20230911982982 booyah db migrate_up
# or
$ booyah db migrate_up 20230911982982
```

* Migrate down a specific version (rollback)

```sh
$ VERSION=20230911982982 booyah db migrate_down
# or
$ booyah db migrate_down 20230911982982
```

* Connecting to the database defined in config/application.yml via command line:

```sh
$ booyah db
```