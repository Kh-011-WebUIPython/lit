from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=150)
    repository = models.ForeignKey('repositories.Repository')
