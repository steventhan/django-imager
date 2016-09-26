from django.conf.urls import url
from .views import ProfileView, MyProfileView


urlpatterns = [
    url(
        r'^(?P<pk>\d+)',
        ProfileView.as_view(),
    ),
    url(
        r'^$',
        MyProfileView.as_view(),
        name='my_profile'
    )
]
