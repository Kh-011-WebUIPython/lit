from rest_framework import serializers

from repositories.models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ('url', 'id', 'name', 'created')
        extra_kwargs = {
            'url': {
                'view_name': 'repositories:repository-detail',
            }
        }
