# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-17 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0006_auto_20171114_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
