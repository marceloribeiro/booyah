from booyah.db.migrate.application_migration import ApplicationMigration

class CreateTableBooyahAttachments(ApplicationMigration):
    def up(self):
        def create_table_and_index():
            self.create_table('booyah_attachments', {
                'id': 'primary_key',
                'record_id': 'integer',
                'record_type': 'string',
                'name': 'string',
                'key': 'string',
                'filename': 'string',
                'extension': 'string',
                'byte_size': 'integer',
                'created_at': 'datetime',
                'updated_at': 'datetime'
            })
            self.add_index('booyah_attachments', ['record_id', 'record_type', 'name'])
        super().up(create_table_and_index)


    def down(self):
        def drop_table_and_index():
            self.drop_index('booyah_attachments', ['record_id', 'record_type', 'name'])
            self.drop_table('booyah_attachments')
        super().down(drop_table_and_index)