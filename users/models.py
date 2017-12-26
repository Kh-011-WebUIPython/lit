import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def get_file_path(instance, filename) -> str:
    """
    Method for generating path for user avatar on local storage

    :param instance: User object
    :param filename: name of uploaded file
    :return: server path relatively defaults storage [lit.settings.base.MEDIA_*]
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('users/avatars', filename)


class User(AbstractUser):
    """
    Base user model depends on default django abstract user model
    """
    avatar = models.ImageField(upload_to=get_file_path,
                               null=True,
                               blank=True)
    background = models.ImageField(blank=True)
    repositories = models.ManyToManyField('repositories.Repository',
                                          related_name='users',
                                          through='permissions.UserPermissions')
