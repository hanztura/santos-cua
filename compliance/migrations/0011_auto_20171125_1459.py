# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-25 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0010_auto_20171118_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_calendar_year',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='client',
            name='month_business_year_end',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=12),
        ),
        migrations.AlterField(
            model_name='client',
            name='date_end',
            field=models.DateField(null=True),
        ),
    ]