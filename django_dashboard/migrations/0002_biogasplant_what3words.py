# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='biogasplant',
            name='what3words',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
