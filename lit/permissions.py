from rest_framework import permissions

from branches.models import Branch
from permissions.models import UserPermissions, PERM_OWNER, PERM_CONTRIB
from repositories.models import Repository

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS', ]


class ReadOnly(permissions.BasePermission):
    """
    The request to only allow read-only operations.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsContributorOrReadOnly(ReadOnly):
    """
    The request is authenticated as a contributor user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
            super(IsContributorOrReadOnly, self).has_permission(request, view) or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        try:
            if isinstance(obj, (Branch, UserPermissions)):
                repo_id = obj.repository_id
            elif isinstance(obj, Repository):
                repo_id = obj.id
            ups = UserPermissions.objects.get(user=request.user,
                                              repository_id=repo_id).status
        except UserPermissions.DoesNotExist as dne:
            return False

        if ups == PERM_CONTRIB:
            if isinstance(obj, Branch):
                if request.method in ['POST', 'PUT', 'DELETE']:
                    return True
                else:
                    return False
            elif isinstance(obj, UserPermissions):
                if request.method in ['DELETE', 'PUT', 'POST']:
                    return False
            elif isinstance(obj, Repository):
                if request.method in ['DELETE', 'PUT']:
                    return False
        elif ups == PERM_OWNER:
            return True

        return False


class IsOwnerOrReadOnly(IsContributorOrReadOnly):
    """
    The request is authenticated as a owner user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return super(IsOwnerOrReadOnly, self).has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        try:
            if isinstance(obj, (Branch, UserPermissions)):
                repo_id = obj.repository_id
            elif isinstance(obj, Repository):
                repo_id = obj.id
            ups = UserPermissions.objects.get(user=request.user,
                                              repository_id=repo_id).status
        except UserPermissions.DoesNotExist as dne:
            return False

        if ups == PERM_OWNER:
            return True
        elif ups == PERM_CONTRIB:
            return super(IsOwnerOrReadOnly, self).has_object_permission(request, view, obj)
        return False
