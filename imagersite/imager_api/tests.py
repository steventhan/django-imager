from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from imager_images.models import Photo
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
        self.photo = PhotoFactory(user=self.user)
        self.photo.save()

    def teardown(self):
        self.user.delete()
        self.photo.delete()

    def test_api_endpoint_authenticated_only(self):
        res = self.client.get(reverse('api_photo'))
        self.assertEqual(res.status_code, 403)
