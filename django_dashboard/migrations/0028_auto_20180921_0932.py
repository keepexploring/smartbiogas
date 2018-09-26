# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-21 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0027_pendingjobs_rejected_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingjobs',
            name='rejected_by',
            field=models.ManyToManyField(blank=True, related_name='techicians_rejected', to='django_dashboard.UserDetail'),
        ),
    ]
