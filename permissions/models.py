from django.db import models

PERM_OWNER = 'o'
PERM_CONTRIB = 'c'

PERMISSIONS = (
    (PERM_OWNER, 'owner'),
    (PERM_CONTRIB, 'contributor')
)


class UserPermissions(models.Model):
    """
    Model to represent version control permissions

    OWNER - a user who can do anything with the repository, pull request, branches, and commits etc.
    CONTRIBUTOR - this user has less permission then repository owner branches, and commits etc.

    Implementation of the lit permissions (see /lit/permissions.py)
    """
    user = models.ForeignKey('users.User')
    repository = models.ForeignKey('repositories.Repository')
    status = models.CharField(max_length=1, choices=PERMISSIONS)

    class Meta:
        unique_together = ('user', 'repository')
