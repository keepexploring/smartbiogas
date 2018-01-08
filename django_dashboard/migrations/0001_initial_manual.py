# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 13:31
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BiogasPlants',
            fields=[
                ('plant_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('town', models.CharField(max_length=200, null=True)),
                ('description_location', models.CharField(max_length=400, null=True)),
                ('postcode', models.CharField(max_length=20, null=True)),
                ('type_biogas', models.CharField(choices=[('TUBULAR', 'tubular'), ('FIXED_DOME', 'fixed_dome')], max_length=20, null=True)),
                ('size_biogas', models.FloatField(null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, db_index=True, geography=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='JobHistory',
            fields=[
                ('job_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('technicians_ids', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None)),
                ('date_flagged', models.DateTimeField(null=True)),
                ('due_date', models.DateTimeField(null=True)),
                ('date_completed', models.DateTimeField(null=True)),
                ('job_status', models.CharField(choices=[('UNASSIGNED', 'unassigned'), ('RESOLVING', 'resolving'), ('ASSISTANCE', 'assistance'), ('OVERDUE', 'overdue'), ('DECOMMISSIONED', 'decommissioned')], default='UNASSIGNED', max_length=16, null=True)),
                ('fault_description', models.TextField(null=True)),
                ('other', models.TextField(null=True)),
                ('client_feedback_star', models.IntegerField(default=None, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('client_feedback_additional', models.TextField(null=True)),
                ('overdue_for_acceptance', models.NullBooleanField(default=False)),
                ('priority', models.NullBooleanField(default=False)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_dashboard.BiogasPlants')),
            ],
            options={
                'get_latest_by': ['-priority', '-date_flagged'],
            },
        ),
        migrations.CreateModel(
            name='Technicians',
            fields=[
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(db_index=True, max_length=15, null=True)),
                ('nearest_town', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('acredit_to_install', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, db_index=True, default=list, null=True, size=None)),
                ('acredited_to_fix', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, db_index=True, default=list, null=True, size=None)),
                ('specialist_skills', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, db_index=True, default=list, null=True, size=None)),
                ('datetime_created', models.DateTimeField(blank=True, db_index=True, editable=False, null=True)),
                ('datetime_modified', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('surname', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, db_index=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, db_index=True, max_length=200, null=True, validators=[django.core.validators.EmailValidator])),
                ('biogas_owner', models.NullBooleanField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Technition_realtime',
            fields=[
                ('technicians', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='django_dashboard.Technicians')),
                ('number_jobs_active', models.IntegerField(blank=True, null=True)),
                ('number_of_jobs_completed', models.IntegerField(blank=True, null=True)),
                ('seconds_active', models.IntegerField(blank=True, null=True)),
                ('status', models.NullBooleanField(db_index=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, db_index=True, geography=True, srid=4326)),
            ],
        ),
        migrations.AddField(
            model_name='biogasplants',
            name='user',
            field=models.ManyToManyField(to='django_dashboard.Users'),
        ),
    ]
