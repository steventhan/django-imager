"""Tests for the Photo and Album models."""
from django.test import TestCase, Client
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
import factory
from django.urls import reverse


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo
    title = factory.Sequence(lambda n: "Photo {}".format(n))


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album
    title = factory.Sequence(lambda n: "Album {}".format(n))


class PhotoTestCase(TestCase):

    def setUp(self):
        self.user = User(username='test_user')
        self.user.save()
        self.photo = PhotoFactory(user=self.user)
        self.photo.save()

    def teardown(self):
        self.user.delete()
        self.profile.delete()

    def test_user_reference(self):
        """Test photo is associated with correct user."""
        self.assertTrue(self.photo.user == self.user)


class AlbumTestCase(TestCase):

    def setUp(self):
        self.user = User(username='test_user')
        self.user.save()
        self.photo = PhotoFactory(user=self.user)
        self.photo.save()
        self.album = AlbumFactory(cover=self.photo, user=self.user)
        self.album.save()
        self.album.photos.add(self.photo)

    def teardown(self):
        self.user.delete()
        self.profile.delete()

    def test_album_photos(self):
        """Test album size."""
        num_photos = self.album.photos.count()
        self.assertTrue(num_photos == 1)

    def test_album_reference(self):
        """Test album referenced to user."""
        self.assertTrue(self.album.user == self.user)

    def test_album_cover(self):
        """Test that there is a cover photo."""
        self.assertTrue(self.album.cover == self.photo)


class AlbumView(TestCase):
    """Test case for registration view."""
    def setUp(self):
        self.response = self.client.get(reverse('albums_list'))
        self.c = Client()
        self.user = User(username='test_user')
        self.user.save()
        self.c.force_login(user=self.user)
        self.logged_in_response = self.c.get(reverse('albums_list'))

    def tearDown(self):
        self.user.delete()

    def test_albums_redirect(self):
        self.assertEquals(self.response.status_code, 302)

    def test_albums_logged_in(self):
        self.assertContains(self.logged_in_response, 'Albums', status_code=200)

    def test_context_albums(self):
        from django.db.models.query import QuerySet
        assert type(self.logged_in_response.context['albums']) is QuerySet
