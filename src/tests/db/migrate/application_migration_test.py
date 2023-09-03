import os
from booyah.db.migrate.application_migration import ApplicationMigration
from booyah.db.adapters.base_adapter import BaseAdapter

class TestApplicationMigration:
    def setup_method(self):
        self.migration = ApplicationMigration()

    def test_init_sets_up_default_values(self):
        self.migration = ApplicationMigration('1')
        assert self.migration.should_run_up
        assert self.migration.should_run_down
        assert not self.migration.success_up
        assert not self.migration.success_down
        assert self.migration.adapter == BaseAdapter.get_instance()
        assert self.migration.version == '1'

    def test_migrations_folder(self):
        assert self.migration.migrations_folder() == f"{os.getenv('ROOT_PROJECT_PATH')}/db/migrate"

    def test_get_migrations(self, mocker):
        mocker.patch.object(self.migration, 'get_migrations', return_value=['1_create_users.py', '2_create_posts.py'])
        migrations = self.migration.get_migrations()
        assert len(migrations) == 2
        assert migrations[0] == '1_create_users.py'
        assert migrations[1] == '2_create_posts.py'

    def test_migrate_all(self, mocker):
        mocker.patch.object(self.migration, 'get_migrations', return_value=['1_create_users.py', '2_create_posts.py'])
        mocked_migrate = mocker.patch.object(ApplicationMigration, 'migrate')
        self.migration.migrate_all()
        assert mocked_migrate.call_count == 2
        assert mocked_migrate.call_args_list == [
            (('1_create_users.py', '1'),),
            (('2_create_posts.py', '2'),)
        ]

    def test_migrate(self, mocker):
        migration_mock = mocker.Mock()
        migration_class_mock = mocker.Mock(return_value=migration_mock)
        mocker.patch.object(self.migration, 'get_migration_class', return_value=migration_class_mock)
        self.migration.migrate('1_create_users.py', '1')
        assert self.migration.get_migration_class.call_count == 1
        assert self.migration.get_migration_class.call_args_list == [
            (('1_create_users.py', 'CreateUsers'),),
        ]
        assert migration_mock.up.call_count == 1

    def test_create_schema_migrations(self, mocker):
        db_adapter_mock = mocker.Mock()
        mocker.patch.object(self.migration, 'adapter', return_value=db_adapter_mock)
        self.migration.create_schema_migrations()
        assert self.migration.adapter.create_schema_migrations.call_count == 1

    def migration_has_been_run(self, mocker):
        db_adapter_mock = mocker.Mock()
        mocker.patch.object(db_adapter_mock, 'migration_has_been_run', return_value=True)
        mocker.patch.object(self.migration, 'adapter', return_value=db_adapter_mock)
        assert self.migration.migration_has_been_run('1')
        assert self.migration.adapter.migration_has_been_run.call_count == 1
        assert self.migration.adapter.migration_has_been_run.call_args_list == [
            (('1',),)
        ]

    def test_before_up(self, mocker):
        mocker.patch.object(self.migration, 'create_schema_migrations')
        mocker.patch.object(self.migration, 'migration_has_been_run', return_value=False)
        self.migration.before_up()
        assert self.migration.create_schema_migrations.call_count == 1
        assert self.migration.migration_has_been_run.call_count == 1
        assert self.migration.should_run_up

    def test_after_up(self, mocker):
        mocker.patch.object(self.migration, 'save_version')
        mocker.patch.object(self.migration.adapter, 'close_connection')
        self.migration.success_up = True
        self.migration.after_up()
        assert self.migration.save_version.call_count == 1
        assert self.migration.adapter.close_connection.call_count == 1

    def test_before_down(self, mocker):
        mocker.patch.object(self.migration, 'migration_has_been_run', return_value=True)
        self.migration.before_down()
        assert self.migration.migration_has_been_run.call_count == 1
        assert self.migration.should_run_down

    def test_after_down(self, mocker):
        mocker.patch.object(self.migration, 'delete_version')
        mocker.patch.object(self.migration.adapter, 'close_connection')
        self.migration.success_down = True
        self.migration.after_down()
        assert self.migration.delete_version.call_count == 1
        assert self.migration.adapter.close_connection.call_count == 1

    def test_up(self, mocker):
        mocker.patch.object(self.migration, 'before_up')
        self.migration.should_run_up = True
        mocker.patch.object(self.migration, 'after_up')
        mocked_block = mocker.Mock()
        self.migration.up(mocked_block)
        assert self.migration.before_up.call_count == 1
        assert mocked_block.call_count == 1
        assert self.migration.after_up.call_count == 1

    def test_up_does_not_run_if_should_run_up_is_false(self, mocker):
        mocker.patch.object(self.migration, 'before_up')
        self.migration.should_run_up = False
        mocker.patch.object(self.migration, 'after_up')
        mocked_block = mocker.Mock()
        self.migration.up(mocked_block)
        assert self.migration.before_up.call_count == 1
        assert mocked_block.call_count == 0
        assert self.migration.after_up.call_count == 1

    def test_down(self, mocker):
        mocker.patch.object(self.migration, 'before_down')
        self.migration.should_run_down = True
        mocker.patch.object(self.migration, 'after_down')
        mocked_block = mocker.Mock()
        self.migration.down(mocked_block)
        assert self.migration.before_down.call_count == 1
        assert mocked_block.call_count == 1
        assert self.migration.after_down.call_count == 1

    def test_down_does_not_run_if_should_run_down_is_false(self, mocker):
        mocker.patch.object(self.migration, 'before_down')
        self.migration.should_run_down = False
        mocker.patch.object(self.migration, 'after_down')
        mocked_block = mocker.Mock()
        self.migration.down(mocked_block)
        assert self.migration.before_down.call_count == 1
        assert mocked_block.call_count == 0
        assert self.migration.after_down.call_count == 1

    def test_save_version(self, mocker):
        self.migration = ApplicationMigration('1')
        mocker.patch.object(self.migration.adapter, 'save_version')
        self.migration.save_version()
        assert self.migration.adapter.save_version.call_count == 1
        assert self.migration.adapter.save_version.call_args_list == [
            (('1',),)
        ]

    def test_delete_version(self, mocker):
        self.migration = ApplicationMigration('1')
        mocker.patch.object(self.migration.adapter, 'delete_version')
        self.migration.delete_version()
        assert self.migration.adapter.delete_version.call_count == 1
        assert self.migration.adapter.delete_version.call_args_list == [
            (('1',),)
        ]

    def test_create_table(self, mocker):
        mocker.patch.object(self.migration.adapter, 'create_table')
        self.migration.create_table('users', {'name': 'string'})
        assert self.migration.adapter.create_table.call_count == 1
        assert self.migration.adapter.create_table.call_args_list == [
            (('users', {'name': 'string'}),)
        ]

    def test_drop_table(self, mocker):
        mocker.patch.object(self.migration.adapter, 'drop_table')
        self.migration.drop_table('users')
        assert self.migration.adapter.drop_table.call_count == 1
        assert self.migration.adapter.drop_table.call_args_list == [
            (('users',),)
        ]

    def test_add_column(self, mocker):
        mocker.patch.object(self.migration.adapter, 'add_column')
        self.migration.add_column('users', 'name', 'string')
        assert self.migration.adapter.add_column.call_count == 1
        assert self.migration.adapter.add_column.call_args_list == [
            (('users', 'name', 'string'),)
        ]

    def test_drop_column(self, mocker):
        mocker.patch.object(self.migration.adapter, 'drop_column')
        self.migration.drop_column('users', 'name')
        assert self.migration.adapter.drop_column.call_count == 1
        assert self.migration.adapter.drop_column.call_args_list == [
            (('users', 'name'),)
        ]

    def test_rename_column(self, mocker):
        mocker.patch.object(self.migration.adapter, 'rename_column')
        self.migration.rename_column('users', 'name', 'first_name')
        assert self.migration.adapter.rename_column.call_count == 1
        assert self.migration.adapter.rename_column.call_args_list == [
            (('users', 'name', 'first_name'),)
        ]

    def test_change_column(self, mocker):
        mocker.patch.object(self.migration.adapter, 'change_column')
        self.migration.change_column('users', 'name', 'string')
        assert self.migration.adapter.change_column.call_count == 1
        assert self.migration.adapter.change_column.call_args_list == [
            (('users', 'name', 'string'),)
        ]

    def test_add_index(self, mocker):
        mocker.patch.object(self.migration.adapter, 'add_index')
        self.migration.add_index('users', 'name')
        assert self.migration.adapter.add_index.call_count == 1
        assert self.migration.adapter.add_index.call_args_list == [
            (('users', 'name'),)
        ]

    def test_remove_index(self, mocker):
        mocker.patch.object(self.migration.adapter, 'remove_index')
        self.migration.remove_index('users', 'name')
        assert self.migration.adapter.remove_index.call_count == 1
        assert self.migration.adapter.remove_index.call_args_list == [
            (('users', 'name'),)
        ]