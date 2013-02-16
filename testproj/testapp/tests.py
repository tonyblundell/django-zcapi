from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.test import TestCase
from django.test.client import Client
import json
from testapp.models import Actor, Movie, Role, MegaModel
from zcapi.utils import JsonResponse
from zcapi.utils import empty_response_on_404, get_model_or_404, to_dict


class JsonResponseTestCase(TestCase):

    def test_mimetype(self):
        """A JSONResponse has a JSON content type header"""
        header = ('Content-Type', 'application/json')
        response = JsonResponse()
        self.assertEqual(response._headers['content-type'], header)

    def test_list(self):
        """A JSONResponse for a list contains valid JSON data"""
        l = [{'a': '1', 'b': '2'}, {'z': '9', 'y': '8'}]
        response = JsonResponse(l)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, l)

    def test_dictionary(self):
        """A JsonResponse for a dictionary contains valid JSON data"""
        d = {'a': '1', 'b': '2'}
        response = JsonResponse(d)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, d)


class EmptyResponseOn404TestCase(TestCase):

    def test__404(self):
        """An empty HttpResponse is returned when Http404 is raised"""
        def f():
            raise Http404
        response = empty_response_on_404(f)()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, '')

    def test_200(self):
        """A regular HttpResponse is passed through as normal"""
        def f():
            return HttpResponse('Hello')
        response = empty_response_on_404(f)()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Hello')


class GetModelOr404TestCase(TestCase):

    def test_valid_model(self):
        """A model object is returned for valid app and model names"""
        m = get_model_or_404('testapp', 'actor')
        self.assertEqual(m, Actor)

    def test_invalid_model(self):        
        with self.assertRaises(Http404):
            m = get_model_or_404('invalid', 'invalid')    


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
        self.tom_dict = {'id': unicode(self.tom.id),
                         'name': self.tom.name,
                         'movies': [{'id': unicode(self.big.id),
                                     'title': self.big.title},
                                    {'id': unicode(self.code.id),
                                     'title': self.code.title}]}
        self.ian_dict = {'id': unicode(self.ian.id),
                         'name': self.ian.name,
                         'movies': [{'id': unicode(self.code.id),
                                     'title': self.code.title},
                                    {'id': unicode(self.rich.id),
                                     'title': self.rich.title}]}
        self.actor_dicts = sorted([self.tom_dict, self.ian_dict])

    def test_get_list(self):
        """A GET request for a model list returns all items"""
        url = reverse('zcapi_list',
            kwargs={'app': 'testapp', 'model': 'actor'})
        response = self.client.get(url)
        data = sorted(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, self.actor_dicts)

    def test_get_item(self):
        """A GET request for a specific item returns the correct item"""
        url = reverse('zcapi_item',
            kwargs={'app': 'testapp', 'model': 'actor', 'pk': self.tom.id})
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, self.tom_dict)


class ApiPostRequestTestCase(TestCase):

    def test_post(self):
        """A POST request creates and returns a new object"""
        url = reverse('zcapi_list',
            kwargs={'app': 'testapp', 'model': 'actor'})
        post_data = {'name': 'Nicolas Cage'}
        response = self.client.post(url, post_data)
        data = json.loads(response.content)
        obj = Actor.objects.get()
        self.assertEqual(unicode(obj.id), data['id'])
        self.assertEqual(obj.name, data['name'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(data.keys()), ['id', 'movies', 'name'])
        self.assertEqual(data['name'], 'Nicolas Cage')
        self.assertEqual(Actor.objects.count(), 1)


class ApiDeleteRequestTestCase(TestCase):

    def test_delete(self):
        """A DELETE request deletes the specified object"""
        michael = Actor.objects.create(name='Michael J Fox')
        christopher = Actor.objects.create(name='Christopher Lloyd')
        url = reverse('zcapi_item',
            kwargs={'app': 'testapp', 'model': 'actor', 'pk': michael.id})
        response = self.client.delete(url)
        ids = [actor.id for actor in Actor.objects.all()]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ids, [christopher.id])


class ApiInvalidRequestTestCase(TestCase):

    def test_get_list_invalid(self):
        """A GET request for a non-existant model returns a 404 response"""
        response = self.client.get('/api/testapp/fakemodel/')
        self.assertEqual(response.status_code, 404)

    def test_get_item_invalid(self):
        """A GET request for a non-existant instance returns a 404 response"""
        response = self.client.get('/api/testapp/actor/1/')
        self.assertEqual(response.status_code, 404)

    def test_post_invalid(self):
        """An incomplete POST request causes an IntegrityError exception"""
        url = reverse('zcapi_list',
            kwargs={'app': 'testapp', 'model': 'actor'})
        post_data = {'not_name': 'Nicolas Cage'}
        with self.assertRaises(IntegrityError):
            self.client.post(url, post_data)
        self.assertEqual(Actor.objects.count(), 0)

    def test_delete_invalid(self):
        """A DELETE request for an invalid instance returns a 404 response"""
        bruce = Actor.objects.create(name="Bruce Willis")
        url = reverse('zcapi_item', 
            kwargs={'app': 'testapp', 'model': 'actor', 'pk': bruce.id + 1})
        response = self.client.delete(url)
        ids = [actor.id for actor in Actor.objects.all()]
        self.assertEqual(response.status_code, 404)
        self.assertEqual(ids, [bruce.id])


class ApiFieldTypeTestCase(TestCase):

    def test_field_types(self):
        """All field types successfully pass through the API"""
        now = datetime.now()
        obj = MegaModel.objects.create(
            big_integer=1, boolean=True, char='Hello',
            comma_separated_integers='1,2,3', date=now, date_time=now,
            decimal=0.5, email='example@example.com', file='hello.txt',
            file_path='hello.txt', floatx=0.5, generic_ip_address='0.0.0.0', 
            image='hello.jpg', integer=1, ip_address='0.0.0.0',
            null_boolean=True, positive_integer=1, positive_small_integer=1,
            slug='hello', small_integer=1, text='hello', time=now,
            url='example.com')
        obj = MegaModel.objects.get(id=obj.id)
        fields = ('big_integer', 'boolean', 'char', 'comma_separated_integers',
            'date', 'date_time', 'decimal', 'email', 'file', 'file_path',
            'floatx', 'image', 'integer', 'ip_address', 'generic_ip_address',
            'null_boolean', 'positive_integer', 'positive_small_integer',
            'slug', 'small_integer', 'text', 'time', 'url')
        url = reverse('zcapi_item', 
            kwargs={'app': 'testapp', 'model': 'megamodel', 'pk': obj.id})
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        for field in fields:
            self.assertEqual(data[field], unicode(getattr(obj, field)))