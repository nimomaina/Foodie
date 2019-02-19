import unittest
from app.models import Blog, User
from app import db


class BlogTest(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username='James', password='potato', email='james@ms.com')
        self.new_blog = Blog(id=12345, title='Title for Blog', author_id=1)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Blog))

    def test_to_check_instance_variables(self):
        self.assertEquals(self.new_blog.id, 12345)
        self.assertEquals(self.new_blog.title, 'Title for pitches')
        self.assertEquals(self.new_blog.author_id, 1)


