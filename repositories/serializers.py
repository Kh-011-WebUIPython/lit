import logging

from rest_framework import serializers

from permissions.models import UserPermissions, PERM_OWNER
from repositories.models import Repository
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)


class RepositorySerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    created = serializers.DateTimeField(format='%Y-%m-%d_%H-%M-%S-%f')

    def create(self, validated_data):
        repository = Repository(name=validated_data.get('name', None),
                                server_path='asdas')  # TODO: describe file saving procedure and find a way to generate server path
        repository.save()
        permission = UserPermissions(user=self.context['request'].user,
                                     repository=repository,
                                     status=PERM_OWNER)
        permission.save()
        return repository

    def update(self, instance, validated_data):
        for field in validated_data:
            instance.__setattr__(field, validated_data.get(field))
        instance.save()
        return instance

    class Meta:
        model = Repository
        fields = ('url', 'id', 'name', 'created', 'users')
        extra_kwargs = {
            'url': {
                'view_name': 'repositories:repository-detail',
            }
        }