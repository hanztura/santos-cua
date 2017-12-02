# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dtr', '0006_auto_20171201_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='log_type',
            field=models.IntegerField(choices=[(1, 'None'), (2, 'In'), (3, 'Out'), (4, 'Overtime - In'), (5, 'Overtime - Out')], default='NA'),
        ),
    ]