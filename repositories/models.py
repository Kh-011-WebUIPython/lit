from django.db import models


class Repository(models.Model):
    name = models.CharField(max_length=150)
    server_path = models.CharField(max_length=4096)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Repositories'
        ordering = ('created',)
