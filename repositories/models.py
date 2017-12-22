from django.db import models


class Repository(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    default_branch = models.ForeignKey('branches.Branch',
                                       related_name='default',
                                       null=True)