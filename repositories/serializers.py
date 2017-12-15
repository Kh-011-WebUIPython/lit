from rest_framework import serializers

from repositories.models import Repository
from users.serializers import UserSerializer


class RepositorySerializer(serializers.ModelSerializer):
    # users = serializers.PrimaryKeyRelatedField(many=True, read_only=True, view_name='user-detail')
    # users = UserSerializer


    class Meta:
        model = Repository
        fields = ('url', 'id', 'name', 'created', 'users')
        extra_kwargs = {
            'url': {
                'view_name': 'repositories:repository-detail',
            }
        }
