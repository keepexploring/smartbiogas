# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-12 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0047_remove_jobhistory_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobhistory',
            name='description_help_need',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobhistory',
            name='reason_abandoning_job',
            field=models.TextField(blank=True, null=True),
        ),
    ]
