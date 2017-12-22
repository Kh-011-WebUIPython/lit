from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(blank=True)
    background = models.ImageField(blank=True)
    repositories = models.ManyToManyField('repositories.Repository',
                                          related_name='users',
                                          through='permissions.UserPermissions')
