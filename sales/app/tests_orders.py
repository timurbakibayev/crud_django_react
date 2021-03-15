from django.test import TestCase
from django.contrib.auth.models import User
import json

test_user = {"username": "testuser", "password": "testpassword"}


class NotesTest(TestCase):
    def setUp(self):
        new_user = User.objects.create(username=test_user["username"])
        new_user.set_password(test_user["password"])
        new_user.save()

    def get_token(self):
        res = self.client.post('/api/token/',
                               data=json.dumps({
                                   'username': test_user["username"],
                                   'password': test_user["password"],
                               }),
                               content_type='application/json',
                               )
        result = json.loads(res.content)
        self.assertTrue("access" in result)
        return result["access"]

    def test_add_orders_forbidden(self):
        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-01-01",
                                   'item': "Hard Drive",
                                   'price': 100,
                                   'quantity': 10,
                               }),
                               content_type='application/json',
                               )
        self.assertEquals(res.status_code, 401)
        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-01-01",
                                   'item': "Hard Drive",
                                   'price': 100,
                                   'quantity': 10,
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer WRONG TOKEN'
                               )
        self.assertEquals(res.status_code, 401)

    def test_add_orders_ok(self):
        token = self.get_token()
        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-01-01",
                                   'item': "Hard Drive",
                                   'price': 100,
                                   'quantity': 10,
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        result = json.loads(res.content)["data"]
        self.assertEquals(result["date"], '2020-01-01')
        self.assertEquals(result["item"], 'Hard Drive')
        self.assertEquals(result["price"], 100)
        self.assertEquals(result["quantity"], 10)

    def test_add_orders_wrong_data(self):
        token = self.get_token()
        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-01-01",
                                   'item': "Hard Drive",
                                   'price': -1,
                                   'quantity': 10,
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-01-01",
                                   'item': "Hard Drive",
                                   'price': 1,
                                   'quantity': -10,
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-01-01",
                                   'item': "",
                                   'price': 1,
                                   'quantity': 10,
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

    def test_add_orders_calculate(self):
        token = self.get_token()
        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-01-01",
                                   'item': "Hard Drive",
                                   'price': 5,
                                   'quantity': 7,
                                   'amount': 10000,  # should be ignored
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        result = json.loads(res.content)["data"]
        self.assertEquals(result["amount"], 35)  # should be calculated
