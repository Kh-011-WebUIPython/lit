from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.CharField(max_length=4096, blank=True)


class UserContributor(models.Model):
    user = models.ForeignKey('users.User')
    repository = models.ForeignKey('repositories.Repository')
