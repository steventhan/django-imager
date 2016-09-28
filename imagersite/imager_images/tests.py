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


class BaseTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User(username='test_user')
        self.user.save()
        self.photo = PhotoFactory(user=self.user)
        self.photo.save()
        self.album = AlbumFactory(cover=self.photo, user=self.user)
        self.album.save()
        self.album.photos.add(self.photo)
        self.c.force_login(user=self.user)

    def tearDown(self):
        self.user.delete()
        self.photo.delete()
        self.album.delete()



class PhotoTestCase(BaseTestCase):

    def test_user_reference(self):
        """Test photo is associated with correct user."""
        self.assertTrue(self.photo.user == self.user)


class AlbumTestCase(BaseTestCase):

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


class AlbumView(BaseTestCase):
    """Test case for registration view."""

    def setUp(self):
        super(AlbumView, self).setUp()
        self.response = self.client.get(reverse('albums_list'))
        self.logged_in_response = self.c.get(reverse('albums_list'))

    def test_albums_redirect(self):
        self.assertEquals(self.response.status_code, 302)

    def test_albums_logged_in(self):
        self.assertContains(self.logged_in_response, 'Albums', status_code=200)

    def test_context_albums(self):
        from django.db.models.query import QuerySet
        self.assertTrue(type(self.logged_in_response.context['albums']) is QuerySet)
        self.assertEqual(len(self.logged_in_response.context['albums']), 1)

    def test_user_association(self):
        self.assertEqual(self.logged_in_response.context['albums'].first().user, self.user)

    def test_logged_in_template(self):
        self.assertTemplateUsed(self.logged_in_response, 'imager_images/albums.html')


class AlbumDetailView(BaseTestCase):
    """Test the album detail view."""

    def setUp(self):
        super(AlbumDetailView, self).setUp()
        self.response = self.client.get(reverse('album_detail', args=(1,)))
        self.logged_in_response = self.c.get(reverse('album_detail', args=(self.album.id,)))

    def test_albums_redirect(self):
        self.assertEquals(self.response.status_code, 302)

    def test_albums_logged_in(self):
        self.assertEquals(self.logged_in_response.status_code, 200)

    def test_logged_in_template(self):
        self.assertTemplateUsed(self.logged_in_response, 'imager_images/album-detail.html')


class PhotosView(BaseTestCase):
    """Test the photos view."""

    def setUp(self):
        super(PhotosView, self).setUp()
        self.response = self.client.get(reverse('photos_list'))
        self.logged_in_response = self.c.get(reverse('photos_list'))

    def test_photos_redirect(self):
        self.assertEquals(self.response.status_code, 302)

    def test_photos_logged_in(self):
        self.assertContains(self.logged_in_response, 'Photos', status_code=200)

    def test_logged_in_template(self):
        self.assertTemplateUsed(self.logged_in_response, 'imager_images/photos.html')
