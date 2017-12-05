from django.db import models
# from users.models import User


class Repository(models.Model):
    name = models.CharField(max_length=150)
    path_on_server = models.CharField(max_length=4096)


class Branch(models.Model):
    STATUS_ACTIVE = 'a'
    STATUS_MERGED = 'm'
    STATUSES = (
        (STATUS_ACTIVE, 'active'),
        (STATUS_MERGED, 'merged'),
    )
    name = models.CharField(max_length=150)
    repository = models.ForeignKey('Repository')
    status = models.CharField(max_length=1, default=STATUS_ACTIVE, choices=STATUSES)


class BranchCommit(models.Model):
    branch = models.ForeignKey('Branch')
    commit = models.ForeignKey('Commit')


class Commit(models.Model):
    user = models.ForeignKey('users.User')
    long_hash = models.ForeignKey('Files')
    short_hash = models.CharField(max_length=6)
    datetime = models.DateTimeField()
    comment = models.CharField(max_length=250)


class Files(models.Model):
    long_hash = models.CharField(max_length=128, primary_key=True)
    snapshot = models.CharField(max_length=4096)  # path to archive