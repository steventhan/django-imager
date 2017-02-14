from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
@python_2_unicode_compatible
class ImagerProfile(models.Model):
    address_1 = models.CharField(
            'Stress Address 1',
            max_length=255,
            blank=True,
            null=True)
    address_2 = models.CharField(
            'Stress Address 2',
            max_length=255,
            blank=True,
            null=True)
    city = models.CharField(
            max_length=128,
            blank=True,
            null=True)
    state = models.CharField(
            max_length=2,
            blank=True,
            null=True)
    zipcode = models.CharField(
            max_length=7,
            blank=True,
            null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    @property
    def is_active(self):
        return self.user.is_active

    def __str__(self):
        fn = self.user.get_full_name().strip() or self.user.get_username()
        return "{}".format(fn)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_imager_profile(sender, **kwargs):
    """Create a imager profile assoc with User if it's a new user."""
    if kwargs['created']:
        ImagerProfile(user=kwargs['instance']).save()
