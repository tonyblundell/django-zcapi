from django.db import IntegrityError
from django.test import TestCase
from django.test.client import Client
import json
from testapp.models import Actor, Movie, Role


class ApiGetRequestTestCase(TestCase):

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
        self.tom_dict = {'id': str(self.tom.id),
                         'name': self.tom.name,
                         'movies': [{'id': str(self.big.id),
                                     'title': self.big.title},
                                    {'id': str(self.code.id),
                                     'title': self.code.title}]}
        self.ian_dict = {'id': str(self.ian.id),
                         'name': self.ian.name,
                         'movies': [{'id': str(self.code.id),
                                     'title': self.code.title},
                                    {'id': str(self.rich.id),
                                     'title': self.rich.title}]}
        self.actor_dicts = sorted([self.tom_dict, self.ian_dict])

    def test_get_list(self):
        """A GET request for a model list returns all items"""
        response = self.client.get('/api/testapp/actor/')
        data = sorted(json.loads(response.content))
        self.assertEqual(data, self.actor_dicts)

    def test_get_item(self):
        """A GET request for a specific item returns the correct item"""
        url = '/api/testapp/actor/{0}/'.format(self.tom.id)
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(data, self.tom_dict)


class ApiPostRequestTestCase(TestCase):

    def test_post(self):
        """A POST request creates and returns a new object"""
        url = '/api/testapp/actor/'
        post_data = {'name': 'Nicolas Cage'}
        response = self.client.post(url, post_data)
        response_data = json.loads(response.content)
        self.assertEqual(sorted(response_data.keys()), ['id', 'movies', 'name'])
        self.assertEqual(response_data['name'], 'Nicolas Cage')
        self.assertEqual(Actor.objects.count(), 1)
        obj = Actor.objects.get()
        self.assertEqual(str(obj.id), response_data['id'])
        self.assertEqual(obj.name, response_data['name'])


class ApiInvalidRequestTestCase(TestCase):

    def test_get_list_invalid(self):
        """A GET request for a non-existant model returns a 404 response"""
        response = self.client.get('/api/testapp/fakemodel/')
        self.assertEqual(response.status_code, 404)

    def test_get_item_invalid(self):
        """A GET request for a non-existant model returns a 404 response"""
        response = self.client.get('/api/testapp/actor/1/')
        self.assertEqual(response.status_code, 404)

    def test_post_invalid(self):
        """An incomplete POST request causes an IntegrityError exception"""
        url = '/api/testapp/actor/'
        post_data = {'not_name': 'Nicolas Cage'}
        with self.assertRaises(IntegrityError):
            self.client.post(url, post_data)