# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 21:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commits', '0001_initial'),
        ('repositories', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('status', models.CharField(choices=[('a', 'active'), ('m', 'merged')], default='a', max_length=1)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repositories.Repository')),
            ],
        ),
        migrations.CreateModel(
            name='BranchCommit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.Branch')),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commits.Commit')),
            ],
        ),
    ]