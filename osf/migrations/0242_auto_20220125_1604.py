# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2022-01-25 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0241_abstractprovider_allow_bulk_uploads'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schemaresponseblock',
            unique_together=set([('source_schema_response', 'schema_key')]),
        ),
        migrations.RemoveField(
            model_name='schemaresponseblock',
            name='source_schema_block',
        ),
    ]
