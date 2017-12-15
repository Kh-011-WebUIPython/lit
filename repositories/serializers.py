import logging

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from permissions.models import UserPermissions, PERM_OWNER
from repositories.models import Repository
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)

class RepositorySerializer(serializers.ModelSerializer):

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
        try:
            userpers = UserPermissions.objects.get(user=self.context['request'].user).status
        except UserPermissions.DoesNotExist as dne:
            raise PermissionDenied from dne

        if userpers == PERM_OWNER:
            for field in validated_data:
                instance.__setattr__(field, validated_data.get(field))
            instance.save()
            return instance
        else:
            raise PermissionDenied

    class Meta:
        model = Repository
        fields = ('url', 'id', 'name', 'created',)
        extra_kwargs = {
            'url': {
                'view_name': 'repositories:repository-detail',
            }
        }
