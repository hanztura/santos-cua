# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-18 07:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20171118_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='date_hired',
            field=models.DateField(default=datetime.datetime(2017, 11, 18, 7, 20, 22, 433252, tzinfo=utc)),
        ),
    ]
