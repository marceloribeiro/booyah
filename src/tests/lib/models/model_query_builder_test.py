from booyah.models.model_query_builder import ModelQueryBuilder
from booyah.models.application_model import ApplicationModel

class User(ApplicationModel):
    pass

class Post(ApplicationModel):
    pass

class TestModelQueryBuilder:
    def setup_method(self):
        self.create_users_table()

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

    def test_all(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.all()
        assert query_builder.select_query == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users'

    def test_find(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.find(1)
        assert query_builder.select_query == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users'
        assert query_builder.where_conditions == ['users.id = 1']

    def test_select_all_columns(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.select_all_columns()
        assert query_builder.select_query == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users'

    def test_select(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.select('name', 'email')
        assert query_builder.select_query == 'SELECT name,email FROM users'

    def test_where(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.where('name = ?', 'Test User')
        assert query_builder.where_conditions == ['name = \'Test User\'']
        query_builder.where('email = ?', 'test@user.com')
        assert query_builder.where_conditions == ['name = \'Test User\'', 'email = \'test@user.com\'']

    def test_where_with_operator(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.where('name', 'Test User')
        assert query_builder.where_conditions == ['name = \'Test User\'']
        query_builder.where('email', 'test@user.com')
        assert query_builder.where_conditions == ['name = \'Test User\'', 'email = \'test@user.com\'']
        query_builder.where('created_at > ?', '2020-01-01')
        assert query_builder.where_conditions == ['name = \'Test User\'', 'email = \'test@user.com\'' , 'created_at > \'2020-01-01\'']
        assert query_builder.build_query() == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users WHERE name = \'Test User\' AND email = \'test@user.com\' AND created_at > \'2020-01-01\''

    def test_quote_if_needed(self):
        query_builder = ModelQueryBuilder(User)
        assert query_builder.quote_if_needed('Test User') == '\'Test User\''
        assert query_builder.quote_if_needed(1) == 1

    def test_build_query(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.select('name', 'email')
        assert query_builder.build_query() == 'SELECT name,email FROM users'
        query_builder.where('name = ?', 'Test User')
        assert query_builder.build_query() == 'SELECT name,email FROM users WHERE name = \'Test User\''
        query_builder.where('email = ?', 'test@user.com')
        assert query_builder.build_query() == 'SELECT name,email FROM users WHERE name = \'Test User\' AND email = \'test@user.com\''
        query_builder.where('created_at > ?', '2020-01-01')
        assert query_builder.build_query() == 'SELECT name,email FROM users WHERE name = \'Test User\' AND email = \'test@user.com\' AND created_at > \'2020-01-01\''
        query_builder.where('age > ?', 18)
        assert query_builder.build_query() == 'SELECT name,email FROM users WHERE name = \'Test User\' AND email = \'test@user.com\' AND created_at > \'2020-01-01\' AND age > 18'

    def test_offset(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.offset(10)
        assert query_builder.build_query() == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users OFFSET 10'

    def test_limit(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.limit(10)
        assert query_builder.build_query() == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users LIMIT 10'

    def test_per_page(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.per_page(10)
        assert query_builder.build_query() == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users LIMIT 10'

    def test_page(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.per_page(10)
        query_builder.page(2)
        assert query_builder.build_query() == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users LIMIT 10 OFFSET 10'

    def test_order(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.order('name ASC')
        query_builder.order('age DESC')
        assert query_builder.build_query() == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users ORDER BY name ASC,age DESC'

    def test_group(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.group('name')
        assert query_builder.build_query() == 'SELECT users.created_at, users.email, users.id, users.name, users.updated_at FROM users GROUP BY name'

    def test_join(self):
        self.create_posts_table()
        query_builder = ModelQueryBuilder(Post)
        query_builder.join('users', 'posts.user_id = users.id')
        assert query_builder.build_query() == 'SELECT posts.content, posts.created_at, posts.id, posts.title, posts.updated_at, posts.user_id FROM posts INNER JOIN users ON (posts.user_id = users.id)'

    def left_join_method(self):
        self.create_posts_table()
        query_builder = ModelQueryBuilder(Post)
        query_builder.left_join('users', 'posts.user_id = users.id')
        assert query_builder.build_query() == 'SELECT posts.id, posts.title, posts.content, posts.user_id, posts.created_at, posts.updated_at FROM posts LEFT JOIN users ON (posts.user_id = users.id)'

    def right_join_method(self):
        self.create_posts_table()
        query_builder = ModelQueryBuilder(Post)
        query_builder.right_join('users', 'posts.user_id = users.id')
        assert query_builder.build_query() == 'SELECT posts.id, posts.title, posts.content, posts.user_id, posts.created_at, posts.updated_at FROM posts RIGHT JOIN users ON (posts.user_id = users.id)'

    def test_results(self):
        self.create_users_sample()
        query_builder = ModelQueryBuilder(User)
        assert len(query_builder.results()) == 3
        assert query_builder.results()[0].name == 'Test User'
        assert query_builder.results()[1].name == 'Another'
        assert query_builder.results()[2].name == 'Third'

    def test_first(self):
        self.create_users_sample()
        query_builder = ModelQueryBuilder(User)
        assert query_builder.first().name == 'Test User'

    def test_last(self):
        self.create_users_sample()
        query_builder = ModelQueryBuilder(User)
        assert query_builder.last().name == 'Third'

    def test_count(self):
        self.create_users_sample()
        query_builder = ModelQueryBuilder(User)
        assert query_builder.count() == 3

    def test_model_from_result(self):
        self.create_users_sample()
        query_builder = ModelQueryBuilder(User)
        result = query_builder.raw_results()[0]
        assert query_builder.model_from_result(result).name == 'Test User'
        assert query_builder.model_from_result(result).email == 'test@email.com'

    def test_cleanup(self):
        query_builder = ModelQueryBuilder(User)
        query_builder.select('name', 'email')
        query_builder.where('name = ?', 'Test User')
        query_builder.where('email = ?', 'test@user.com')
        query_builder.where('created_at > ?', '2020-01-01')
        query_builder.where('age > ?', 18)
        query_builder.offset(10)
        query_builder.limit(10)
        query_builder.order('name ASC')
        query_builder.group('name')
        query_builder.cleanup()
        assert query_builder.select_query == ''
        assert query_builder.where_conditions == []
        assert query_builder._offset == None
        assert query_builder._limit == None
        assert query_builder.order_by_attributes == []
        assert query_builder.group_by_attributes == []