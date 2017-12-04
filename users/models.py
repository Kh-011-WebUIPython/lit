from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from repositories.models import Repository


class User(AbstractUser):
    avatar = models.CharField(max_length=4096, blank=True)
    repositories = models.ManyToManyField('Repository', related_name='users', through='UserPermissions')


class UserPermissions(Permission):
    user = models.ForeignKey('User')
    repository = models.ForeignKey(Repository)

