# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-24 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0072_auto_20180521_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='UICtoDeviceID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UIC', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('device_id', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('biogas_plant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userdetail', to='django_dashboard.BiogasPlant')),
            ],
        ),
    ]
