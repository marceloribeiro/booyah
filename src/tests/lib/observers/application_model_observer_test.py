from booyah.models.application_model import ApplicationModel
from booyah.models.helpers import *

class BlogPostLog:
    @classmethod
    def singleton(self):
        if not hasattr(self, 'instance'):
            self.instance = BlogPostLog()
        return self.instance

    def __init__(self) -> None:
        self.actions_called = []

class BlogPost(ApplicationModel):
    after_validation('after_validation_called')
    before_validation('before_validation_called')
    before_save('before_save_called')
    after_save('after_save_called')
    before_create('before_create_called')
    after_create('after_create_called')
    before_update('before_update_called')
    after_update('after_update_called')
    before_destroy('before_destroy_called')
    after_destroy('after_destroy_called')

    def __init__(self, attributes={}):
        super().__init__(attributes)
        self.post_log = BlogPostLog.singleton()

    def before_validation_called(self):
        self.post_log.actions_called.append('before_validation_called')
      
    def after_validation_called(self):
        self.post_log.actions_called.append('after_validation_called')
    
    def before_save_called(self):
        self.post_log.actions_called.append('before_save_called')
    
    def after_save_called(self):
        self.post_log.actions_called.append('after_save_called')
    
    def before_create_called(self):
        self.post_log.actions_called.append('before_create_called')
    
    def after_create_called(self):
        self.post_log.actions_called.append('after_create_called')
    
    def before_update_called(self):
        self.post_log.actions_called.append('before_update_called')
    
    def after_update_called(self):
        self.post_log.actions_called.append('after_update_called')
    
    def before_destroy_called(self):
        self.post_log.actions_called.append('before_destroy_called')
    
    def after_destroy_called(self):
        self.post_log.actions_called.append('after_destroy_called')
    
class TestApplicationModelObserver:
    def setup_method(self):
        self.create_posts_table()

    def create_posts_table(self):
        BlogPost.drop_table()
        BlogPost.create_table({
            'id': 'primary_key',
            'title': 'string',
            'content': 'string',
            'slug': 'string',
            'is_published': 'boolean',
            'created_at': 'datetime',
            'updated_at': 'datetime'
        })
    
    def test_before_validation_call(self):
        post = BlogPost()
        post.valid()
        assert 'before_validation_called' in BlogPostLog.singleton().actions_called
    
    def test_after_validation_call(self):
        post = BlogPost()
        post.valid()
        assert 'after_validation_called' in BlogPostLog.singleton().actions_called
    
    def test_before_save_call(self):
        post = BlogPost()
        post.save()
        assert 'before_save_called' in BlogPostLog.singleton().actions_called

    def test_after_save_call(self):
        post = BlogPost()
        post.save()
        assert 'after_save_called' in BlogPostLog.singleton().actions_called
    
    def test_before_create_call(self):
        post = BlogPost.create({})
        assert 'before_create_called' in BlogPostLog.singleton().actions_called
    
    def test_after_create_call(self):
        post = BlogPost.create({})
        assert 'after_create_called' in BlogPostLog.singleton().actions_called
    
    def test_before_update_call(self):
        post = BlogPost.create({})
        post.update({'title': 'New Title'})
        assert 'before_update_called' in BlogPostLog.singleton().actions_called
    
    def test_after_update_call(self):
        post = BlogPost.create({})
        post.update({'title': 'New Title'})
        assert 'after_update_called' in BlogPostLog.singleton().actions_called
    
    def test_before_destroy_call(self):
        post = BlogPost.create({})
        post.destroy()
        assert 'before_destroy_called' in BlogPostLog.singleton().actions_called
    
    def test_after_destroy_call(self):
        post = BlogPost.create({})
        post.destroy()
        assert 'after_destroy_called' in BlogPostLog.singleton().actions_called