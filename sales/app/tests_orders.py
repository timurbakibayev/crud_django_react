from django.test import TestCase
from django.contrib.auth.models import User
import json

test_user = {"username": "testuser", "password": "testpassword"}


class OrdersTest(TestCase):
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

    #  -------------------------- GET RECORDS -------------------------------------------

    def test_get_records(self):
        token = self.get_token()
        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-01-01",
                                   'item': "Hard Drive",
                                   'price': 5,
                                   'quantity': 7,
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        id1 = json.loads(res.content)["data"]["id"]

        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-02-02",
                                   'item': "Monitor",
                                   'price': 20,
                                   'quantity': 30,
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        id2 = json.loads(res.content)["data"]["id"]

        res = self.client.get('/api/orders/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )

        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)["data"]
        self.assertEquals(len(result), 2)  # 2 records
        self.assertTrue(result[0]["id"] == id1 or result[1]["id"] == id1)
        self.assertTrue(result[0]["id"] == id2 or result[1]["id"] == id2)

        res = self.client.get(f'/api/orders/{id1}/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)["data"]
        self.assertEquals(result["date"], '2020-01-01')
        self.assertEquals(result["item"], 'Hard Drive')
        self.assertEquals(result["price"], 5)
        self.assertEquals(result["quantity"], 7)
        self.assertEquals(result["amount"], 35)


    #  -------------------------- PUT AND DELETE RECORDS --------------------------------------

    def test_put_delete_records(self):
        token = self.get_token()
        res = self.client.post('/api/orders/',
                               data=json.dumps({
                                   'date': "2020-01-01",
                                   'item': "Hard Drive",
                                   'price': 5,
                                   'quantity': 7,
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        id = json.loads(res.content)["data"]["id"]

        res = self.client.put(f'/api/orders/{id}/',
                               data=json.dumps({
                                   'date': "2020-02-02",
                                   'item': "Monitor",
                                   'price': 50,
                                   'quantity': 70,
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )

        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)["data"]
        self.assertEquals(result["date"], '2020-02-02')

        res = self.client.get(f'/api/orders/{id}/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)["data"]
        self.assertEquals(result["date"], '2020-02-02')
        self.assertEquals(result["item"], 'Monitor')
        self.assertEquals(result["price"], 50)
        self.assertEquals(result["quantity"], 70)
        self.assertEquals(result["amount"], 3500)

        res = self.client.delete(f'/api/orders/{id}/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 410)  # Gone

        res = self.client.get(f'/api/orders/{id}/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 404)  # Not found
