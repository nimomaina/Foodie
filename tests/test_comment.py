import unittest
from app.models import Comment, User,Blog
from app import db


class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_James = User(username='James', password='potato', email='james@ms.com')
        self.post_Fly = Blog(title='James', body='potato', id='1')
        self.new_comment = Comment(body='good', author='John Doe')

    def tearDown(self):
        Comment.query.delete()
        Post.query.delete()
        User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_to_check_instance_variables(self):
        self.assertEquals(self.new_comment.body, 'good')
        self.assertEquals(self.new_comment.author, 'John Doe')



