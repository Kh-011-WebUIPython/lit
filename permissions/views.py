from rest_framework import generics

from permissions.models import UserPermissions
from permissions.serializers import PermissionSerializer


class PermissionList(generics.ListCreateAPIView):
    queryset = UserPermissions.objects.all()
    serializer_class = PermissionSerializer


class PermissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPermissions.objects.all()
    serializer_class = PermissionSerializer
