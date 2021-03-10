from django.test import TestCase
from django.contrib.auth.models import User
import json

test_users = [
    {"username": "testuser1", "password": "testpassword1"},
    {"username": "testuser2", "password": "testpassword2"},
]

class LoginTest(TestCase):
    def setUp(self):
        for user in test_users:
            new_user = User.objects.create(username=user["username"])
            new_user.set_password(user["password"])
            new_user.save()

    def test_login(self):
        USER1 = test_users[0]
        res = self.client.post('/api/token/',
                               data=json.dumps({
                                   'username': USER1["username"],
                                   'password': USER1["password"],
                               }),
                               content_type='application/json',
                               )
        result = json.loads(res.content)
        self.assertTrue("access" in result)
