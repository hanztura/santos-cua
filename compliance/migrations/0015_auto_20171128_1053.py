# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 02:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0014_clientattachments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientattachments',
            name='code',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
