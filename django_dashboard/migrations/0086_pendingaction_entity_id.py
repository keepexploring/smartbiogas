# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-01 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0085_auto_20180629_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingaction',
            name='entity_id',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]
