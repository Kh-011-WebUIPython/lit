from django.db import models

class Branch(models.Model):
    STATUS_ACTIVE = 'a'
    STATUS_MERGED = 'm'
    STATUSES = (
        (STATUS_ACTIVE, 'active'),
        (STATUS_MERGED, 'merged'),
    )
    name = models.CharField(max_length=150)
    repository = models.ForeignKey('repositories.Repository')
    status = models.CharField(max_length=1, default=STATUS_ACTIVE, choices=STATUSES)


class BranchCommit(models.Model):
    branch = models.ForeignKey('branches.Branch')
    commit = models.ForeignKey('commits.Commit')