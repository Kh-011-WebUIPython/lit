import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('users/avatars', filename)


class User(AbstractUser):
    avatar = models.ImageField(upload_to=get_file_path,
                               null=True,
                               blank=True)
    background = models.ImageField(blank=True)
    repositories = models.ManyToManyField('repositories.Repository',
                                          related_name='users',
                                          through='permissions.UserPermissions')
