# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-14 04:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='photo',
            field=models.ImageField(upload_to='/media/tutors/'),
        ),
    ]
