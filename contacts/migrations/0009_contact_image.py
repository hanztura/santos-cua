# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_auto_20171116_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='contacts/images/'),
        ),
    ]
