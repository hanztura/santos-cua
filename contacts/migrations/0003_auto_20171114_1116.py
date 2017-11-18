# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20171102_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='person',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.IntegerField(blank=True, choices=[(1, 'CDO'), (2, 'CEB'), (2, 'MNL')], null=True),
        ),
    ]