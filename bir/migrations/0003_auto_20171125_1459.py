# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-25 06:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bir', '0002_auto_20171103_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birformschedule',
            name='bir_form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='bir.BirForm'),
        ),
    ]
