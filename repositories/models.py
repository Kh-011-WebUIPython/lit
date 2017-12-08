from django.db import models
# from users.models import User


class Repository(models.Model):
    name = models.CharField(max_length=150)
    server_path = models.CharField(max_length=4096)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('users.User')

    class Meta:
        db_table = 'Repositories'
        ordering = ('created',)
