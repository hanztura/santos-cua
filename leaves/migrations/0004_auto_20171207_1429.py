# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0003_auto_20171207_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuance',
            name='valid_on_year',
            field=models.DateField(choices=[(2017, 2017), (2018, 2018)], default=2017, verbose_name='From'),
        ),
    ]
