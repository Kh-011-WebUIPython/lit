import logging

from rest_framework import serializers

from lit.parameterised_hyperlinkedidentityfield import ParameterisedHyperlinkedIdentityField
from permissions.models import UserPermissions, PERM_CONTRIB, PERMISSIONS
from users.models import User

logger = logging.getLogger(__name__)


class PermissionSerializer(serializers.Serializer):
    """
    Permission serializer needs for render base permission fields(url, id, username, status)

    :model UserPermissions
    """

    id = serializers.ReadOnlyField()
    url = ParameterisedHyperlinkedIdentityField(view_name='permissions:permission-detail',
                                                lookup_fields=(
                                                    ('repository_id', 'repository_id'), ('pk', 'permission_id')),
                                                read_only=True)
    status = serializers.CharField(read_only=True)
    username = serializers.SerializerMethodField()

    def create(self, validated_data: dict) -> UserPermissions:
        """
        Add permission to repository for user

        :param validated_data: data form http request
        :return: UserPermission object
        """
        """ 
        XXX For getting uses initial_data without validations, DRF can't pass username to validated_data after is_valid [bad style] 
            Reason: (Problem with validating SerializerMethodField read_only)
        """
        if not User.objects.filter(username=self.initial_data['username']).exists():
            raise serializers.ValidationError("User with '%s' username does not exist" % self.initial_data['username'])

        user = User.objects.filter(username=self.initial_data['username']).first()

        if UserPermissions.objects.filter(user_id=user.pk, repository_id=self.context['repository_id'],
                                          status=PERM_CONTRIB).exists():
            raise serializers.ValidationError("User '%s' already have permissions" % self.initial_data['username'])

        user_permission = UserPermissions(user_id=user.pk,
                                          repository_id=self.context['repository_id'],
                                          status=PERM_CONTRIB)
        user_permission.save()
        return user_permission

    def update(self, instance: UserPermissions, validated_data: dict) -> UserPermissions:
        """ In case of extending permission system for repositories """
        raise NotImplementedError("In future release")

    def to_representation(self, instance: UserPermissions) -> dict:
        """
        Needs for modifying fields value

        :param instance: UserPermissions object
        :return: dict with modified field
        """
        result = super().to_representation(instance)

        """ Convert 'status' from short notation to human-readable  """
        for short_permission, long_permission in PERMISSIONS:
            if result['status'] == short_permission:
                result['status'] = long_permission
                break

        return result

    def get_username(self, instance: UserPermissions):
        """
        Returning username

        :param instance: UserPermission object
        :return: username
        """
        return instance.user.username
