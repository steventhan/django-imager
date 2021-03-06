# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 23:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0006_modify_related_names_album_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='imager_images.Photo'),
        ),
        migrations.AlterField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='photos', to='imager_images.Photo'),
        ),
    ]
