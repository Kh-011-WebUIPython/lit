from rest_framework import permissions

from branches.models import Branch
from permissions.models import UserPermissions, PERM_OWNER, PERM_CONTRIB


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    The request is authenticated as a owner user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        try:
            repo_id = obj.id
            if isinstance(obj, Branch):
                repo_id = obj.repository_id
            ups = UserPermissions.objects.get(user=request.user,
                                              repository_id=repo_id).status
        except UserPermissions.DoesNotExist as dne:
            return False
        return ups == PERM_OWNER


class IsContributorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    The request is authenticated as a contributor user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        try:
            repo_id = obj.id
            if isinstance(obj, Branch):
                repo_id = obj.repository_id
            ups = UserPermissions.objects.get(user=request.user,
                                              repository_id=repo_id).status
        except UserPermissions.DoesNotExist as dne:
            return False

        return ups == PERM_CONTRIB


class ReadOnly(permissions.BasePermission):
    """
    The request to only allow read-only operations.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
