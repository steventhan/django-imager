from django.conf.urls import url
from .views import PhotoView, AlbumView


urlpatterns = [
    url(
        r'^photos/',
        PhotoView.as_view(),
        name='photos-list'
    ),
    url(
        r'^albums/',
        AlbumView.as_view(),
        name='albums-list'
    ),
]
