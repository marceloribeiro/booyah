from booyah.models.application_model import ApplicationModel

class User(ApplicationModel):
    pass

class Post(ApplicationModel):
    pass

class TestApplicationModel:
    def create_users_table(self):
        User.drop_table()
        User.create_table({
            'id': 'primary_key',
            'name': 'string',
            'email': 'string',
            'created_at': 'datetime',
            'updated_at': 'datetime'
        })

    def create_posts_table(self):
        Post.drop_table()
        Post.create_table({
            'id': 'primary_key',
            'title': 'string',
            'content': 'string',
            'user_id': 'integer',
            'created_at': 'datetime',
            'updated_at': 'datetime'
        })


    def create_user(self, name='Test User', email='test@email.com'):
        User.create({
            'name': name,
            'email': email,
        })

    def create_post(self, title='Test Post', content='Test Content', user_id=1):
        Post.create({
            'title': title,
            'content': content,
            'user_id': user_id,
        })

    def create_users_sample(self):
        self.create_users_table()
        self.create_user()
        self.create_user(name='Another', email='another@email.com')
        self.create_user(name='Third', email='third@email.com')

    def create_posts_sample(self):
        self.create_users_sample()
        self.create_posts_table()
        self.create_post(user_id=User.first().id)
        self.create_post(title='Another Post', content='Another Content', user_id=User.first().id)
        self.create_post(title='Third Post', content='Third Content', user_id=User.last().id)

    def test_table_name(self):
        assert User.table_name() == 'users'

    def test_create_table(self):
        self.create_users_table()
        assert User.db_adapter().table_columns(User.table_name()).sort() == ['id', 'name', 'email'].sort()

    def test_drop_table(self):
        User.drop_table()
        assert User.db_adapter().table_columns(User.table_name()) == []

    def test_table_columns(self):
        self.create_users_table()
        assert User.get_table_columns().sort() == ['id', 'name', 'email'].sort()

    def test_query_builder(self):
        assert User.query_builder().model_class == User

    def test_all(self):
        self.create_users_sample()
        assert len(User.all()) == 3
        assert User.all().count() == 3
        assert User.first().name == 'Test User'
        assert User.last().name == 'Third'

    def test_find(self):
        self.create_users_sample()
        assert User.find(1).name == 'Test User'
        assert User.find(2).name == 'Another'
        assert User.find(3).name == 'Third'

    def test_where(self):
        self.create_users_sample()
        assert User.where('name', 'Test User').first().name == 'Test User'
        assert User.where('name', 'Another').first().name == 'Another'
        assert User.where('name', 'Third').first().name == 'Third'
        assert User.where('name', 'Fourth').first() == None

    def test_chained_where(self):
        self.create_users_sample()
        assert User.where('name', 'Test User').where('email', 'test').first() == None
        assert User.where('name', 'Test User').where('email', 'test@email.com').first().name == 'Test User'
        assert User.where('name', 'Another').where('email', 'another@email.com').first().name == 'Another'
        assert User.where('name', 'Third').where('email', 'third@email.com').first().name == 'Third'
        assert User.where('name', 'Fourth').where('email', 'fourth').first() == None

    def test_where_with_operator(self):
        self.create_users_sample()
        assert User.where('name = ?', 'Test User').first().name == 'Test User'
        assert User.where('name = ?', 'Another').first().name == 'Another'
        assert User.where('name = ?', 'Third').first().name == 'Third'
        assert User.where('name = ?', 'Fourth').first() == None

    def test_chained_where_with_operator(self):
        self.create_users_sample()
        assert User.where('name = ?', 'Test User').where('email = ?', 'test').first() == None
        assert User.where('name = ?', 'Test User').where('email = ?', 'test@email.com').first().name == \
            'Test User'
        assert User.where('name = ?', 'Another').where('email = ?', 'another').first() == None

    def test_join(self):
        self.create_posts_sample()
        assert Post.join('users', 'posts.user_id = users.id').where('users.name', 'Test User').first().title == \
            'Test Post'
        assert Post.join('users', 'posts.user_id = users.id').where('users.name', 'Another').first() == None
        assert Post.join('users', 'posts.user_id = users.id').where('users.name', 'Third').first().title == \
            'Third Post'

    def test_save(self):
        self.create_users_table()
        user = User({
            'name': 'Test User',
            'email': 'test',
        })
        user.save()
        assert user.id == 1
        assert user.name == 'Test User'
        assert user.email == 'test'
        assert user.created_at != None
        assert user.updated_at != None

    def test_save_with_existing_id(self):
        self.create_users_table()
        self.create_users_sample()
        user = User({
            'id': 1,
            'name': 'Test User Updated',
            'email': 'test@updated.com',
        })
        user.save()
        assert user.id == 1
        assert user.name == 'Test User Updated'
        assert user.email == 'test@updated.com'
        assert user.created_at != None
        assert user.updated_at != None

    def test_create(self):
        self.create_users_table()
        user = User.create({
            'name': 'Test User',
            'email': 'test@email.com',
        })
        assert user.id == 1
        assert user.name == 'Test User'
        assert user.email == 'test@email.com'
        assert user.created_at != None
        assert user.updated_at != None

    def test_update(self):
        self.create_users_sample()
        user = User.find(1)
        previous_updated_at = user.updated_at
        user.update({
            'name': 'Updated Name',
            'email': None
        })
        assert user.name == 'Updated Name'
        assert user.email == None
        assert user.updated_at != None
        assert user.updated_at != previous_updated_at

    def test_patch_update(self):
        self.create_users_sample()
        user = User.find(1)
        previous_updated_at = user.updated_at
        user.patch_update({
            'name': 'Updated Name',
            'email': None
        })
        assert user.name == 'Updated Name'
        assert user.email != None
        assert user.updated_at != None
        assert user.updated_at != previous_updated_at

    def test_destroy(self):
        self.create_users_sample()
        user = User.find(1)
        user.destroy()
        assert User.find(1) == None
        assert User.all().count() == 2