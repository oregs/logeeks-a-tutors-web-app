# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-13 20:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_auto_20170713_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_initialized',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Initialization Date'),
        ),
    ]