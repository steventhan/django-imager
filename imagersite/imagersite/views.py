from django.contrib.auth import views
from registration.backends.hmac.views import RegistrationView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse


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
