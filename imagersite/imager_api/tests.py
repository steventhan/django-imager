from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from imager_images.models import Photo
from django.core.files.base import ContentFile
import factory


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo
    title = factory.Sequence(lambda n: "Photo {}".format(n))
    image = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'test.jpg'
        )
    )


class ImagerApiTestCase(TestCase):
    """Tests for Imager API"""
    def setUp(self):
        self.user = User(username='test_user')
        self.user.save()
        self.c = Client()
        self.c.force_login(user=self.user)
        self.photo = PhotoFactory(user=self.user)
        self.photo.save()

    def teardown(self):
        self.user.delete()
        self.photo.delete()

    def test_api_endpoint_unauthorized(self):
        res = self.client.get(reverse('api_photo', args=('v1', )))
        data = res.json()
        self.assertEqual(res.status_code, 403)
        self.assertTrue('Authentication credentials were not provided' in data['detail'])

    def test_api_endpoint_authenticated(self):
        res = self.c.get(reverse('api_photo', args=('v1', )))
        self.assertEqual(res.status_code, 200)

    def test_api_endpoint_return_json(self):
        res = self.c.get(reverse('api_photo', args=('v1', )))
        data = res.json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)

    def test_api_endpoint_list_photos(self):
        res = self.c.get(reverse('api_photo', args=('v1', )))
        data = res.json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)

    def test_api_endpoint_list_photos_after_added_new_photo(self):
        PhotoFactory(user=self.user, title='test').save()
        res = self.c.get(reverse('api_photo', args=('v1', )))
        data = res.json()
        self.assertEqual(len(data), 2)

    def test_api_endpoint_show_photos_belonged_to_logged_in_user(self):
        another_user = User(username='test_user1')
        another_user.save()
        self.c.force_login(user=another_user)
        res = self.c.get(reverse('api_photo', args=('v1', )))
        data = res.json()
        self.assertEqual(len(data), 0)
