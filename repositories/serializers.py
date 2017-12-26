import logging

from rest_framework import serializers

from lit.parameterised_hyperlinkedidentityfield import ParameterisedHyperlinkedIdentityField
from permissions.models import UserPermissions, PERM_OWNER
from repositories.models import Repository
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)


class RepositorySerializer(serializers.ModelSerializer):
    """
    This class serialize main repository fields(url, id, users, name, description, default branch, etc)
    """
    users = UserSerializer(many=True, read_only=True)
    url = ParameterisedHyperlinkedIdentityField(view_name='repositories:repository-detail',
                                                lookup_fields=(('pk', 'repository_id'),),
                                                read_only=True)

    def create(self, validated_data: dict) -> Repository:
        """
        Overrated method for implement own permission logic on repository create

        :param validated_data: fields from http request for creating repository
        :return: reference on new repository instance
        """
        repository = Repository(name=validated_data.get('name', None),
                                description=validated_data.get('description', None))
        repository.save()
        permission = UserPermissions(user=self.context['request'].user,
                                     repository=repository,
                                     status=PERM_OWNER)
        permission.save()
        return repository

    def update(self, instance: Repository, validated_data: dict) -> Repository:
        """
         Overrated method for implement own logic on repository update

        :param instance: repository object
        :param validated_data: updated fields from http request
        :return: updated repository object
        """
        for field in validated_data:
            instance.__setattr__(field, validated_data.get(field))
        instance.save()
        return instance

    class Meta:
        model = Repository
        fields = ('url', 'id', 'name', 'description', 'users',)
