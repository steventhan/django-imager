"""Tests for the Photo and Album models."""
from django.test import TestCase
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
import factory


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
