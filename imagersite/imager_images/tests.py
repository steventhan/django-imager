"""Tests for the Photo and ALbum Models."""
from django.test import TestCase
from imager_images.models import Photo, Album
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User
import factory


#class UserFactory(factory.django.DjangoModelFactory):
#    class Meta:
#        model = User

#    username = factory.Sequence(lambda n: "user{}".format(n))
#    email = factory.Sequence(
#        lambda n: "user{}@example.com".format(n)
#    )


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo
    title = 'Test Photo'


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album
    title = 'Test Album'


class PhotoTestCase(TestCase):
    def setUp(self):
        self.user = User(username='test_user')
        self.user.save()
        self.profile = ImagerProfile(user=self.user)
        self.profile.save()
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
        self.profile = ImagerProfile(user=self.user)
        self.profile.save()
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
        length = self.album.photos.count()
        self.assertTrue(length == 1)

    def test_album_reference(self):
        """Test album referenced to user."""
        self.assertTrue(self.album.user == self.user)
