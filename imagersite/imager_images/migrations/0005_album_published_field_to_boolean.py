# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0004_adjust_album_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]