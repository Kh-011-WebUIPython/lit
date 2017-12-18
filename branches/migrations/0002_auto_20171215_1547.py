# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 13:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commits', '0001_initial'),
        ('branches', '0001_initial'),
        ('repositories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchcommit',
            name='commit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commits.Commit'),
        ),
        migrations.AddField(
            model_name='branch',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repositories.Repository'),
        ),
    ]