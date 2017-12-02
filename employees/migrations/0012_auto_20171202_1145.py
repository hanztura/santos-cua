# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 03:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0011_auto_20171130_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salaries', to='employees.Employee', verbose_name='Name'),
        ),
    ]
