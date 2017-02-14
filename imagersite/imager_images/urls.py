from django.conf.urls import url
from .views import (PhotoView,
                    AlbumView,
                    AlbumDetailView,
                    UploadPhotoView,
                    AddAlbumView,
                    PhotoDetailView,
                    EditPhotoView,
                    EditAlbumView,
                    )


urlpatterns = [
    url(
        r'^photos/$',
        PhotoView.as_view(),
        name='photos_list'
    ),
    url(
        r'^photos/(?P<pk>\d+)/$',
        PhotoDetailView.as_view(),
        name='photo_detail'
    ),
    url(
        r'^photos/upload/$',
        UploadPhotoView.as_view(),
        name='upload_photo'
    ),
    url(
        r'^photos/(?P<pk>\d+)/edit/$',
        EditPhotoView.as_view(),
        name='edit_photo'
    ),
    url(
        r'^albums/(?P<pk>\d+)/edit/$',
        EditAlbumView.as_view(),
        name='edit_album'
    ),
    url(
        r'^library/$',
        AlbumView.as_view(),
        name='albums_list'
    ),
    url(
        r'^albums/add/$',
        AddAlbumView.as_view(),
        name='add_album'
    ),
    url(
        r'^albums/(?P<pk>\d+)/$',
        AlbumDetailView.as_view(),
        name='album_detail'
    ),
]
