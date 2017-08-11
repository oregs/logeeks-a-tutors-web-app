# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-15 11:19
from __future__ import unicode_literals

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0021_auto_20170715_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('photo', '760x760', adapt_rotation=False, allow_fullsize=True, free_crop=True, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropping'),
        ),
    ]
