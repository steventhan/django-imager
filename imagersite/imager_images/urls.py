from django.conf.urls import url
from .views import (PhotoView,
                    AlbumView,
                    AlbumDetailView,
                    UploadPhotoView,
                    AddAlbumView,
                    PhotoDetailView,
                    )


urlpatterns = [
    url(
        r'^photos/$',
        PhotoView.as_view(),
        name='photos_list'
    ),
    url(
        r'^photo/(?P<pk>\d+)/$',
        PhotoDetailView.as_view(),
        name='photo_detail'
    ),
    url(
        r'^photos/upload/$',
        UploadPhotoView.as_view(),
        name='upload_photo'
    ),
    url(
        r'^library/$',
        AlbumView.as_view(),
        name='albums_list'
    ),
    url(
        r'^album/add/$',
        AddAlbumView.as_view(),
        name='add_album'
    ),
    url(
        r'^album/(?P<pk>\d+)/$',
        AlbumDetailView.as_view(),
        name='album_detail'
    ),
]
