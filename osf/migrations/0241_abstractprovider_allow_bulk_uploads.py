# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2021-12-16 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0240_merge_20211110_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractprovider',
            name='allow_bulk_uploads',
            field=models.NullBooleanField(default=False),
        ),
    ]
