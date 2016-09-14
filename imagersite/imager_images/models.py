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
    published = models.CharField(
            max_length=7,
            blank=True,
            null=True)
    image = models.ImageField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

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
    published = models.CharField(
            max_length=7,
            blank=True,
            null=True)
    cover = models.OneToOneField(Photo, related_name='cover_set')
    photos = models.ManyToManyField(Photo, related_name='photo_set')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "{}: {}".format(self.title, self.user.username)
