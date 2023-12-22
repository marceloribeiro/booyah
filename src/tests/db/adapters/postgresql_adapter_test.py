from booyah.db.adapters.postgresql.postgresql_adapter import PostgresqlAdapter
import pytest
import os

class TestPostgresqlAdapter:
  @pytest.fixture(autouse=True)
  def run_around_tests(self):
      self.adapter = PostgresqlAdapter.get_instance(True)
      self.create_test_table()
      yield
      self.adapter.execute('DROP TABLE IF EXISTS test_table', False)
      self.adapter.close_connection()

  def test_load_config(self):
    from booyah.framework import Booyah
    db_config = Booyah.env_config['database']
    assert self.adapter.host == db_config['host']
    assert self.adapter.port == db_config['port']
    assert self.adapter.user == db_config['username']
    assert self.adapter.password == db_config['password']
    assert self.adapter.database == db_config['database']

  def test_connect(self):
    assert self.adapter.connect() != None

  def test_close_connection(self):
    self.adapter.connect()
    assert self.adapter.connection != None
    self.adapter.close_connection()
    assert self.adapter.connection == None

  def test_execute(self):
    assert self.adapter.execute('SELECT 1') == (1,)

  def test_create_table(self):
    assert self.adapter.execute('SELECT * FROM test_table') == None

  def test_fetch(self):
    self.adapter.execute('INSERT INTO test_table (name) VALUES (\'test\')', False)
    assert self.adapter.fetch('SELECT id, name FROM test_table') == [(1, 'test')]

  def test_get_table_columns(self):
    assert self.adapter.get_table_columns('test_table') == ['created_at', 'id', 'name', 'updated_at']

  def test_insert(self):
    self.adapter.insert('test_table', {'name': 'test'})
    assert self.adapter.fetch('SELECT id, name FROM test_table') == [(1, 'test')]

  def test_update(self):
    self.adapter.insert('test_table', {'name': 'test'})
    self.adapter.update('test_table', 1, {'name': 'test2'})
    assert self.adapter.fetch('SELECT id, name FROM test_table') == [(1, 'test2')]

  def test_delete(self):
    self.adapter.insert('test_table', {'name': 'test'})
    self.adapter.delete('test_table', 1)
    assert self.adapter.fetch('SELECT * FROM test_table') == []

  def create_test_table(self):
    self.adapter.execute('DROP TABLE IF EXISTS test_table', False)
    self.adapter.execute('CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(255), created_at TIMESTAMP, updated_at TIMESTAMP)', False)

  def test_create_and_drop_database(self):
    self.adapter.create_database('db_test_create')
    self.adapter.drop_database('db_test_create')

  def test_use_system_database(self):
    previous_db = self.adapter.database
    self.adapter.use_system_database()
    assert self.adapter.database == 'postgres'
    self.adapter.database = previous_db