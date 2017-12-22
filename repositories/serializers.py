import logging

from rest_framework import serializers

from lit.parameterised_hyperlinkedidentityfield import ParameterisedHyperlinkedIdentityField
from permissions.models import UserPermissions, PERM_OWNER
from repositories.models import Repository
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)


class RepositorySerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    url = ParameterisedHyperlinkedIdentityField(view_name='repositories:repository-detail',
                                                lookup_fields=(('pk', 'repository_id'),),
                                                read_only=True)

    def create(self, validated_data):
        repository = Repository(name=validated_data.get('name', None),
                                description=validated_data.get('description', None))
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
        fields = ('url', 'id', 'name', 'description', 'users', )