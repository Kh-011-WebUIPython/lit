from django.db import models


class Commit(models.Model):
    user = models.ForeignKey('users.User')
    long_hash = models.CharField(max_length=256)
    branch = models.ManyToManyField('branches.Branch')
    commit_time = models.DateTimeField()
    comment = models.CharField(max_length=250)

    @property
    def short_hash(self):
        ''' Calculating short hash '''
        return self.long_hash[:10]

    # class Meta:
    #     unique_together = (('logn_hash', 'id'), )
