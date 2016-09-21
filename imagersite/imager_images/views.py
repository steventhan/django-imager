from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import Photo, Album


@method_decorator(login_required, name='dispatch')
class PhotoView(ListView):
    template_name = 'imager_images/photos.html'
    model = Photo
    context_object_name = 'photos'

    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)
        context['MEDIA_ROOT'] = settings.MEDIA_ROOT
        return context


@method_decorator(login_required, name='dispatch')
class AlbumView(ListView):
    template_name = 'imager_images/albums.html'
    model = Album
    context_object_name = 'albums'
