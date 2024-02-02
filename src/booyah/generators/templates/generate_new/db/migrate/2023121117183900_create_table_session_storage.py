from booyah.db.migrate.application_migration import ApplicationMigration

class CreateTableSessionStorage(ApplicationMigration):
    def up(self):
        super().up(lambda: self.create_table('session_storage', {
            'id': 'primary_key',
            'session_id': 'string',
            'data': 'text',
            'expires_at': 'datetime',
            'created_at': 'datetime',
            'updated_at': 'datetime'
        }))

    def down(self):
        super().down(lambda: self.drop_table('session_storage'))