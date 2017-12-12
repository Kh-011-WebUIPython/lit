from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.CharField(max_length=4096, blank=True)
    repositories = models.ManyToManyField('repositories.Repository', related_name='users', through='permissions.UserPermissions')
