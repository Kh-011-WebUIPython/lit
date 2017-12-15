from rest_framework import serializers

from permissions.models import UserPermissions
from users.serializers import UserSerializer


class PermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = UserPermissions
        fields = ('url', 'id', 'user', 'repository', 'status')
        extra_kwargs = {
            'url': {
                'view_name': 'permissions:permission-detail',
            }
        }
