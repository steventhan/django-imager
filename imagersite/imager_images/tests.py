"""Tests for the Photo and Album models."""
from django.test import TestCase, Client
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import factory
from django.urls import reverse
import os
from io import open


TEST_MEDIA_SOURCE_FILE = os.path.dirname(__file__) + '/test_media/salmon-cookies.png'

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


class UploadPhotoView(BaseTestCase):
    """Test the upload photo view."""

    def setUp(self):
        super(UploadPhotoView, self).setUp()
        self.response = self.client.get(reverse('upload_photo'))
        self.logged_in_response = self.c.get(reverse('upload_photo'))

    def test_template_renders_logged_in(self):
        self.assertTemplateUsed(self.logged_in_response, 'imager_images/upload_photo.html')

    def test_form_in_context(self):
        self.assertTrue(str(type(self.logged_in_response.context['form'])) == "<class 'django.forms.widgets.PhotoForm'>")

    def test_valid_post(self):
        with open(TEST_MEDIA_SOURCE_FILE, 'rb') as fh:
            data = {
                'image': fh,
                'title': 'hello',
            }

            post_response = self.c.post(reverse('upload_photo'), data)
        photo = Photo.objects.last()
        self.assertEqual(photo.user, self.user)
        self.assertEqual(photo.title, 'hello')


class AddAlbumView(BaseTestCase):
    """Test add album view."""

    def setUp(self):
        super(AddAlbumView, self).setUp()
        self.response = self.client.get(reverse('add_album'))
        self.logged_in_response = self.c.get(reverse('add_album'))

    def test_template_renders_logged_in(self):
        self.assertTemplateUsed(self.logged_in_response, 'imager_images/add_album.html')

    def test_form_in_context(self):
        self.assertTrue(str(type(self.logged_in_response.context['form'])) == "<class 'django.forms.widgets.AlbumForm'>")

    def test_valid_post(self):
        data = {
            'title': 'hello',
            'photos': self.photo.pk
        }
        post_response = self.c.post(reverse('add_album'), data)
        self.assertEqual(post_response.status_code, 302)
        album = Album.objects.last()
        self.assertEqual(album.user, self.user)
        self.assertEqual(album.title, 'hello')


class EditPhotoTestCase(BaseTestCase):
    """Test edit album view."""

    def setUp(self):
        super(EditPhotoTestCase, self).setUp()
        self.response = self.client.get(reverse('edit_photo', args=(self.photo.pk, )))
        self.logged_in_response = self.c.get(reverse('edit_photo', args=(self.photo.pk, )))

    def test_redirect_when_not_logged_in(self):
        self.assertEquals(self.response.status_code, 302)

    def test_template_renders_logged_in(self):
        self.assertTemplateUsed(
            self.logged_in_response,
            'imager_images/edit_photo.html'
        )

    def test_form_in_context(self):
        self.assertTrue('form' in self.logged_in_response.context.keys())

    def test_valid_post(self):
        data = {
            'title': 'edited',
            'description': 'edited',
        }
        post = self.c.post(reverse('edit_photo', args=(self.photo.pk, )), data)
        self.assertEqual(post.status_code, 302)
        photo = Photo.objects.last()
        self.assertEqual(photo.title, 'edited')
        self.assertEqual(photo.description, 'edited')

class EditAlbumTestCase(BaseTestCase):
    """Test the edit album view."""
    def setUp(self):
        super(EditAlbumTestCase, self).setUp()
        self.response = self.client.get(reverse('edit_album', args=(self.album.pk, )))
        self.logged_in_response = self.c.get(reverse('edit_album', args=(self.album.pk)))

    def test_redirect_when_not_logged_in(self):
        self.assertEquals(self.response.status_code, 302)

    def test_template_renders_logged_in(self):
        self.assertTemplateUsed(
            self.logged_in_response,
            'imager_images/edit_album.html'
        )

    def test_form_in_context(self):
        self.assertTrue('form' in self.logged_in_response.context.keys())

    def test_valid_post(self):
        data = {
            'title': 'edited album title',
            'description': 'edited album description',
        }
        post = self.c.post(reverse('edit_album', args=(self.album.pk, )), data)
        self.assertEqual(post.status_code, 302)
        album = Album.objects.last()
        self.assertEqual(album.title, 'edited album title')
        self.assertEqual(album.description, 'edited album description')
