from django.test import TestCase
from imager_images.models import Photo, Album
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User

# Create your tests here.
class PhotoTestCase(TestCase):
    def setUp(self):
        self.user = User(username='test_user')
        self.user.save()
        self.profile = ImagerProfile(user=self.user)
        self.profile.save()
        self.photo = Photo(user=self.user)
        self.photo.title = 'test title'
        self.photo.save()

    def teardown(self):
        self.user.delete()
        self.profile.delete()
        self.photo.delete()

    def test_user_reference(self):
        """Test photo is associated with correct user."""
        self.assertTrue(self.photo.user == self.user)


class AlbumTestCase(TestCase):
    def setUp(self):
        self.user = User(username='test_user')
        self.user.save()
        self.profile = ImagerProfile(user=self.user)
        self.profile.save()
        self.photo = Photo(user=self.user)
        self.photo.title = 'test title'
        self.photo.save()
        self.album = Album(user=self.user)
        self.album.title = 'test user album'
        self.album.cover = self.photo
        self.album.save()
        self.album.photos.add(self.photo)

    def teardown(self):
        self.user.delete()
        self.profile.delete()
        self.photo.delete()

    def test_album_photos(self):
        """Test album size."""
        length = self.album.photos.count()
        self.assertTrue(length == 1)

    def test_album_reference(self):
        """Test album referenced to user."""
        self.assertTrue(self.album.user == self.user)
