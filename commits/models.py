from django.db import models
from branches.models import Branch


class Commit(models.Model):
    user = models.ForeignKey('users.User')
    long_hash = models.ForeignKey('commits.Files')
    short_hash = models.CharField(max_length=6)
    commit_time = models.DateTimeField()
    comment = models.CharField(max_length=250)
    branch = models.ManyToManyField(Branch)

class Files(models.Model):
    long_hash = models.CharField(max_length=128, primary_key=True)
    snapshot = models.CharField(max_length=4096)  # path to archive
