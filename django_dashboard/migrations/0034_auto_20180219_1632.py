# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-19 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0033_auto_20180219_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingjobs',
            name='accepted',
            field=models.NullBooleanField(db_index=True, default=None),
        ),
    ]
