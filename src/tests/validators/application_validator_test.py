from booyah.validators.application_validator import ApplicationValidator
from booyah.models.application_model import ApplicationModel

class User(ApplicationModel):
    EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    validates = [
        { 'name': { 'presence': True } },
        { 'email': { 'presence': True, 'format': EMAIL_PATTERN, 'length': {
            'minimum': 10,
            'maximum': 20
        } } },
        { 'ssn': { 'uniqueness': True } },
        { 'age': { 'comparison': {
            'greater_than': 16,
            'less_than': 100,
            'greater_than_or_equal_to': 17,
            'less_than_or_equal_to': 99,
            'not_equal_to': 19
        } } }
    ]

class TestApplicationModel:
    def create_users_table(self):
        User.drop_table()
        User.create_table({
            'id': 'primary_key',
            'name': 'string',
            'email': 'string',
            'ssn': 'string',
            'age': 'integer',
            'created_at': 'datetime',
            'updated_at': 'datetime'
        })

    def setup_method(self):
        self.create_users_table()

    def test_presence_validator(self):
        user = User({'email': 'johndoe@email.com', 'age': 18})
        assert user.valid() == False
        assert user.errors == [{ 'name': 'must be present' }]
        user.name = 'John'
        assert user.valid() == True
        assert user.errors == []

    def test_format_validator(self):
        user = User({'name': 'John', 'email': 'invalid_email', 'age': 18})
        assert user.valid() == False
        assert user.errors == [{ 'email': 'format is invalid' }]
        user.email = 'johndoe@email.com'
        assert user.valid() == True

    def test_uniqueness_validator(self):
        user = User({ 'name': 'John', 'email': 'johndoe@email.com', 'ssn': '1231231234', 'age': 18})
        assert user.valid() == True
        user.save()
        user = User({ 'name': 'Another', 'email': 'another@email.com', 'ssn': '1231231234', 'age': 18})
        assert user.valid() == False
        assert user.errors == [{ 'ssn': 'must be unique' }]

    def test_comparison_validator(self):
        user = User({ 'name': 'John', 'email': 'johndoe@email.com', 'age': 15 })
        assert user.valid() == False
        assert { 'age': 'must be greater than 16' } in user.errors
        user.age = 17
        assert user.valid() == True
        user.age = 100
        assert user.valid() == False
        assert { 'age': 'must be less than 100' } in user.errors
        user.age = 99
        assert user.valid() == True
        user.age = 16
        assert user.valid() == False
        assert { 'age': 'must be greater than or equal to 17' } in user.errors
        user.age = 18
        assert user.valid() == True
        user.age = 19
        assert user.valid() == False

    def test_length_validator(self):
        user = User({ 'name': 'John', 'email': 'je@em.com', 'age': 18 })
        assert user.valid() == False
        assert { 'email': 'must be at least 10 characters' } in user.errors
        user.email = 'johndoejohndoe@email.com'
        assert user.valid() == False
        assert { 'email': 'must be at most 20 characters' } in user.errors
        user.email = 'johndoe@email.com'
        assert user.valid() == True

    def test_save(self):
        user = User({ 'name': 'John', 'email': 'johndoe@email.com', 'age': 14 })
        assert user.is_new_record() == True
        assert user.save() == False
        assert user.is_new_record() == True
        user.age = 18
        assert user.save() != False
        assert user.is_new_record() == False
        assert user.errors == []

    def test_create(self):
        user = User.create({ 'name': 'John', 'email': 'johndoe@email.com', 'age': 15 })
        assert user.is_new_record() == True
        user.age = 18
        assert user.save() != False
        assert user.is_new_record() == False

    def test_update(self):
        user = User.create({ 'name': 'John', 'email': 'johndoe@email.com', 'age': 18 })
        assert user.is_new_record() == False
        user.update({ 'age': 15 })
        assert user.is_new_record() == False
        assert user.age == 15
        assert user.valid() == False