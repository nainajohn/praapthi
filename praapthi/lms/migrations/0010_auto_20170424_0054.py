# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0009_auto_20170424_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_schedules',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2),
        ),
    ]
