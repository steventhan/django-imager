"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.generic.base import TemplateView
from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf import settings
from .views import CustomLoginView, CustomRegistrationView, home_view


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_view, name='home'),
    url(r'^accounts/login/$', CustomLoginView.as_view()),
    url(r'^accounts/register/$', CustomRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^profile/', include('imager_profile.urls')),
    url(r'^images/', include('imager_images.urls')),
    url(r'^api/', include('imager_api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
