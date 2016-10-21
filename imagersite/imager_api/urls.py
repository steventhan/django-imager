from django.conf.urls import url
from imager_api.views import PhotoViewSet


urlpatterns = [
    url(
        r'^(?P<version>(v1))/photo/$',
        PhotoViewSet.as_view({'get': 'list'}),
        name='api_photo',
    ),
]
