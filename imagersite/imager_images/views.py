from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import Photo, Album
from .forms import PhotoForm, AlbumForm


@method_decorator(login_required, name='dispatch')
class PhotoView(ListView):
    template_name = 'imager_images/photos.html'
    model = Photo
    context_object_name = 'photos'

    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)
        context['MEDIA_ROOT'] = settings.MEDIA_ROOT
        return context

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user).all()


@method_decorator(login_required, name='dispatch')
class AlbumView(ListView):
    template_name = 'imager_images/albums.html'
    model = Album
    context_object_name = 'albums'

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user).all()

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        context['MEDIA_ROOT'] = settings.MEDIA_ROOT
        return context


@method_decorator(login_required, name='dispatch')
class AlbumDetailView(DetailView):
    template_name = 'imager_images/album-detail.html'
    model = Album
    context_object_name = 'album'

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user, id=self.kwargs['pk'])


@method_decorator(login_required, name='dispatch')
class UploadPhotoView(CreateView):
    template_name = 'imager_images/upload_photo.html'
    model = Photo
    fields = ['title', 'description', 'image', 'user']
    success_url = '/'
