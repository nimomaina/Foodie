import unittest
from app.models import User
from app import db


class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_user = User(password='banana')
        self.new_user = User(username='John Doe')

    def test_password_setter(self):
        self.assertTrue(self.new_user.password_hash is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('banana'))

    def test_to_check_instance_variables(self):
        self.assertEquals(self.new_user.username, 'John Doe')
        self.assertEquals(self.new_user.password, 'banana')

