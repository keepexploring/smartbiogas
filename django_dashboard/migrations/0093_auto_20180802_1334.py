# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-02 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0092_auto_20180802_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicatorstemplate',
            name='description',
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='indicatorstemplate',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
