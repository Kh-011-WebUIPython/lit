from django.db import models

PERM_OWNER = 'o'
PERM_CONTRIB = 'c'

PERMISSIONS = (
    (PERM_OWNER, 'owner'),
    (PERM_CONTRIB, 'contributor')
)


class UserPermissions(models.Model):
    user = models.ForeignKey('users.User')
    repository = models.ForeignKey('repositories.Repository')
    status = models.CharField(max_length=1, choices=PERMISSIONS)
