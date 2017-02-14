
from django.forms import ModelForm
from .models import Photo, Album


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        exclude = []


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        exclude = []
