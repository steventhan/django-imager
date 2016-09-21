from django.conf.urls import url
from .views import ProfileView


urlpatterns = [
    url(r'^(?P<pk>\d+)', ProfileView.as_view(), name='imager_profile/profile.html'),
]
