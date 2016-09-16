from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings


# Create your models here.
@python_2_unicode_compatible
class ImagerProfile(models.Model):
    active = models.BooleanField(default=False)
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
        return self.active

    def __str__(self):
        fn = self.user.get_full_name().strip() or self.user.get_username()
        return "{}: {}".format(fn, self.card_number)
