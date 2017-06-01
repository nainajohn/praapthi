# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 18:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0012_auto_20170425_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course_created_by',
            name='lecturer_id',
        ),
        migrations.AddField(
            model_name='course_created_by',
            name='institution_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lms.Institution'),
        ),
    ]
