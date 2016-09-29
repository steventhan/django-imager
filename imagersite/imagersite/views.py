from django.contrib.auth import views
from registration.backends.hmac.views import RegistrationView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from imager_images.models import Photo
from django.shortcuts import render
from .settings import MEDIA_URL


class CustomLoginView(TemplateView):
    def get(self, request):
        """Redirect when user logged in."""
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('my_profile'))
        else:
            return views.login(request)

    def post(self, request):
        return views.login(request)


class CustomRegistrationView(RegistrationView):
    """Redirect when user logged in."""
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('my_profile'))
        return super().get(request)


def home_view(request):

    random_pic = Photo.objects.filter(published=True).order_by('?').first()
    try:
        random_pic_url = random_pic.image.url
    except AttributeError:
        random_pic_url = '/'
    context = {
        'page_title': 'Home',
        'picture': random_pic_url,
    }
    return render(request, 'imagersite/index.html', context)
