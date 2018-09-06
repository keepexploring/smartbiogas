# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-04 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0008_auto_20180903_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicatorobjects',
            options={'verbose_name': 'Indicator Object', 'verbose_name_plural': 'Indicator Objects'},
        ),
        migrations.AlterField(
            model_name='pendingjobs',
            name='accepted',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
