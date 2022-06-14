import unittest

from app.auth.models import User
from app.models import Post
from . import BaseTestClass

class PostModelTestCase(BaseTestClass):
    """Suite de tests del modelo Post"""
    
    def test_title_slug(self):
        with self.app.app_context():
            admin = User.get_by_email('admin@xyz.com')
            post = Post(user_id=admin.id, title='Post de prueba', content='Lorem Ipsum')
            post.save()
            self.assertEqual('post-de-prueba', post.title_slug)