# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_auto_20171116_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.IntegerField(blank=True, choices=[(1, 'CDO'), (2, 'CEB'), (3, 'MNL')], null=True),
        ),
    ]