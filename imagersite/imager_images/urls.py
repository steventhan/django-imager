from django.conf.urls import url
from .views import PhotoView, AlbumView, AlbumDetailView, UploadPhotoView


urlpatterns = [
    url(
        r'^photos/$',
        PhotoView.as_view(),
        name='photos_list'
    ),
    url(
        r'^photos/new/$',
        UploadPhotoView.as_view(),
        name='upload_photo'
    ),
    url(
        r'^albums/$',
        AlbumView.as_view(),
        name='albums_list'
    ),
    url(
        r'^albums/(?P<pk>\d+)/$',
        AlbumDetailView.as_view(),
        name='album_detail'
    ),
]
