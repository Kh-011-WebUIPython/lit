from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
# from repositories.models import Repository


class User(AbstractUser):
    avatar = models.CharField(max_length=4096, blank=True)
    repositories = models.ManyToManyField('repositories.Repository', related_name='users', through='UserPermissions')


class UserPermissions(Permission):
    PERM_OWNER = 'o'
    PERM_USER = 'u'
    PERM_CONTRIB = 'c'

    PERMISSIONS = (
        (PERM_OWNER, 'owner'),
        (PERM_USER, 'user'),
        (PERM_CONTRIB, 'contributor')
    )
    user_id = models.ForeignKey('User', default=None)
    repository = models.ForeignKey('repositories.Repository', default=None)
    status = models.CharField(max_length=1, default=PERM_USER, choices=PERMISSIONS)
