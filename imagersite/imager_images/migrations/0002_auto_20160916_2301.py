# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-16 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0001_photo_and_album_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='images/%Y-%m-%d'),
        ),
    ]