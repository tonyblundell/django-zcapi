from django.test import TestCase
from django.test.client import Client
import json
from testapp.models import Actor, Movie, Role


class ApiTestCase(TestCase):

    def setUp(self):
        self.tom = Actor.objects.create(name="Tom Hanks")
        self.ian = Actor.objects.create(name="Ian McKellen")
        self.big = Movie.objects.create(title="Big")
        self.code = Movie.objects.create(title="The Da Vinci Code")
        self.rich = Movie.objects.create(title="Richard III")
        self.tom_in_big = Role.objects.create(actor=self.tom, movie=self.big)
        self.tom_in_code = Role.objects.create(actor=self.tom, movie=self.code)
        self.ian_in_code = Role.objects.create(actor=self.ian, movie=self.code)
        self.ian_in_rich = Role.objects.create(actor=self.ian, movie=self.rich)
        self.client = Client()

    def test_list(self):
        response = self.client.get('/api/testapp/role/')
        data = json.loads(response.content)
        self.assertEqual(len(data), 4)

    def test_item(self):
        url = '/api/testapp/actor/{0}/'.format(self.tom.id)
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(data['name'], "Tom Hanks")