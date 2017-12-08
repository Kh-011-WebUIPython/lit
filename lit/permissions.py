from rest_framework.permissions import BasePermission


# todo: implement
class IsContributor(BasePermission):
    def has_permission(self, request, view):
        return True
