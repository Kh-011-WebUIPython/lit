# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0002_auto_20171222_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
