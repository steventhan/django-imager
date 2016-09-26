from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.urls import reverse


def custom_login(request):
    """Redirect when user logged in."""
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('my_profile'))
    else:
        return views.login(request)
