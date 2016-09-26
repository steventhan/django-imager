from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import ImagerProfile


@method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):
    template_name = 'imager_profile/profile.html'
    model = ImagerProfile
    context_object_name = 'profile'


@method_decorator(login_required, name='dispatch')
class MyProfileView(TemplateView):
    template_name = 'imager_profile/my_profile.html'
