# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-19 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0031_auto_20180216_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingJobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('datetime_created', models.DateTimeField(blank=True, db_index=True, editable=False, null=True)),
                ('job_details', models.TextField(blank=True, null=True)),
                ('accepted', models.BooleanField(db_index=True, default=False)),
                ('biogas_plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_dashboard.BiogasPlant')),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_dashboard.UserDetail')),
            ],
        ),
        migrations.AddField(
            model_name='jobhistory',
            name='date_accepted',
            field=models.DateTimeField(blank=True, db_index=True, editable=False, null=True),
        ),
    ]
