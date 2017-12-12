from rest_framework import serializers
from .models import PERMISSIONS
from permissions.models import UserPermissions


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissions
        fields = ('url', 'id', 'user', 'repository', 'status')
        extra_kwargs = {
            'url': {
                'view_name': 'permissions:permission-detail',
            }
        }
