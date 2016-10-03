from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

# Create your models here.
@python_2_unicode_compatible
class Photo(models.Model):
    title = models.CharField(
            max_length=128,
            blank=True,
            null=True)
    description = models.CharField(
            max_length=500,
            blank=True,
            null=True)
    date_uploaded = models.DateTimeField(
            auto_now_add=True,
            null=False)
    date_modified = models.DateTimeField(
            null=True)
    date_published = models.DateTimeField(
            null=True)
    published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/%Y-%m-%d')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return "{}: {}".format(self.title, self.user.username)


@python_2_unicode_compatible
class Album(models.Model):
    title = models.CharField(
            max_length=128,
            blank=True,
            null=True)
    description = models.CharField(
            max_length=500,
            blank=True,
            null=True)
    date_created = models.DateTimeField(
            auto_now_add=True,
            null=False)
    date_published = models.DateTimeField(
            null=True)
    date_modified = models.DateTimeField(
            null=True)
    published = models.BooleanField(default=False)
    cover = models.OneToOneField(Photo, null=True, blank=True)
    photos = models.ManyToManyField(Photo, related_name='photos')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return "{}: {}".format(self.title, self.user.username)
