# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-20 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0006_auto_20170515_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='lga1',
            field=models.CharField(choices=[('apapa', 'apapa'), ('ajah', 'ajah'), ('bariga', 'bariga'), ('ebute-meta', 'ebute-meta'), ('eti-osa', 'eti-osa'), ('festac', 'festac'), ('gbagada', 'gbagada'), ('ibeju-lekki', 'ibeju-lekki'), ('ifako-ijaye', 'ifako-ijaye'), ('ikeja', 'ikeja'), ('ikorodu', 'ikorodu'), ('ikoyi-obalende', 'ikoyi-obalende'), ('ilupeju', 'ilupeju'), ('ketu', 'ketu'), ('kosofe', 'kosofe'), ('lagos-island', 'lagos-island'), ('lagos-mainland', 'lagos-mainland'), ('magodo', 'magodo'), ('onipanu', 'onipanu'), ('oshodi-isolo', 'oshodi-isolo'), ('somolu', 'somolu'), ('surulere', 'surulere'), ('victoria-island', 'victoria-island')], default='Invalid_lga', max_length=100),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='lga2',
            field=models.CharField(choices=[('apapa', 'apapa'), ('ajah', 'ajah'), ('bariga', 'bariga'), ('ebute-meta', 'ebute-meta'), ('eti-osa', 'eti-osa'), ('festac', 'festac'), ('gbagada', 'gbagada'), ('ibeju-lekki', 'ibeju-lekki'), ('ifako-ijaye', 'ifako-ijaye'), ('ikeja', 'ikeja'), ('ikorodu', 'ikorodu'), ('ikoyi-obalende', 'ikoyi-obalende'), ('ilupeju', 'ilupeju'), ('ketu', 'ketu'), ('kosofe', 'kosofe'), ('lagos-island', 'lagos-island'), ('lagos-mainland', 'lagos-mainland'), ('magodo', 'magodo'), ('onipanu', 'onipanu'), ('oshodi-isolo', 'oshodi-isolo'), ('somolu', 'somolu'), ('surulere', 'surulere'), ('victoria-island', 'victoria-island')], default='Invalid_lga', max_length=100),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='lga3',
            field=models.CharField(choices=[('apapa', 'apapa'), ('ajah', 'ajah'), ('bariga', 'bariga'), ('ebute-meta', 'ebute-meta'), ('eti-osa', 'eti-osa'), ('festac', 'festac'), ('gbagada', 'gbagada'), ('ibeju-lekki', 'ibeju-lekki'), ('ifako-ijaye', 'ifako-ijaye'), ('ikeja', 'ikeja'), ('ikorodu', 'ikorodu'), ('ikoyi-obalende', 'ikoyi-obalende'), ('ilupeju', 'ilupeju'), ('ketu', 'ketu'), ('kosofe', 'kosofe'), ('lagos-island', 'lagos-island'), ('lagos-mainland', 'lagos-mainland'), ('magodo', 'magodo'), ('onipanu', 'onipanu'), ('oshodi-isolo', 'oshodi-isolo'), ('somolu', 'somolu'), ('surulere', 'surulere'), ('victoria-island', 'victoria-island')], default='Invalid_lga', max_length=100),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='subject',
            field=models.CharField(choices=[('Mathematics', 'Mathematics'), ('English', 'English Language'), ('Biology', 'Biology'), ('Physics', 'Physics'), ('Chemistry', 'Chemistry'), ('Further Maths', 'Further Maths'), ('Computer Studies', 'Computer Studies'), ('Technical Drawing', 'Technical Drawing')], max_length=20),
        ),
    ]
