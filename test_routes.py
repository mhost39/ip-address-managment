from unittest import TestCase
import string
import random

from app import app as application


class TestApplication(TestCase):

    @staticmethod
    def random_string():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10))

    @staticmethod
    def info(message):
        print(message)

    def setUp(self):
      self.client = application.app.test_client()

    def test_home_path(self):
      r = self.client.get('/')
      self.assertEqual(r.status_code, 200)
