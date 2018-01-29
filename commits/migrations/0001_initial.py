# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-29 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branches', '0002_branch_repository'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_hash', models.CharField(max_length=256)),
                ('commit_time', models.DateTimeField()),
                ('comment', models.CharField(max_length=250)),
                ('branch', models.ManyToManyField(to='branches.Branch')),
            ],
        ),
    ]
