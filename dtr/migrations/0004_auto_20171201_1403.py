# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 06:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtr', '0003_auto_20171201_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='timetable',
            new_name='timetables',
        ),
    ]