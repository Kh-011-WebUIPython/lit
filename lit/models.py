from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=128)  # length of SHA-3 hash
    ssh = models.CharField(max_length=500, blank=True)
    # TODO: add path for default avatar or make blank=True
    avatar = models.CharField(max_length=300)  # enough to store the path
    backup_email = models.CharField(max_length=80, blank=True)
    repositories = models.ManyToManyField('Repository', related_name='users',
                                          through='UserPermissions')


class Repository(models.Model):
    name = models.CharField(max_length=150)
    path_on_server = models.CharField(max_length=300)


class UserPermissions(models.Model):
    user = models.ForeignKey(User)
    repository = models.ForeignKey(Repository)
    status = models.CharField(max_length=20)  # contributor, owner, user

    class Meta:
        unique_together = (('user', 'repository'), )


class Files(models.Model):
    long_hash = models.CharField(max_length=128, primary_key=True)
    snapshot = models.CharField(max_length=300)  # path to archive


class Commit(models.Model):
    user = models.ForeignKey(User)
    long_hash = models.ForeignKey(Files)
    short_hash = models.CharField(max_length=6)
    datetime = models.DateTimeField()
    comment = models.CharField(max_length=250)


class Branch(models.Model):
    name = models.CharField(max_length=150)
    repository = models.ForeignKey(Repository)
    status = models.CharField(max_length=6, null=True)  # Active or NULL


class BranchCommit(models.Model):
    branch = models.ForeignKey(Branch)
    commit = models.ForeignKey(Commit)