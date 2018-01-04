import logging

from django.http import Http404, HttpResponseForbidden
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from lit.permissions import IsOwnerOrReadOnly
from permissions.models import UserPermissions
from permissions.serializers import PermissionSerializer

logger = logging.getLogger(__name__)


class PermissionList(APIView):
    """
    View for handle GET and POST methods on repository permission
    """
    serializer_class = PermissionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        This method needs for handle GET request on permission-list endpoint and return all permissions object for
        specific repository

        :param request: http request
        :param args: other  parameters
        :param kwargs: dict parsed url variables {repository_id:id}
        :return: json with all permissions for repository
        """
        permissions = UserPermissions.objects.filter(repository_id=kwargs['repository_id'])
        serializer = PermissionSerializer(permissions, context={'request': Request(request)}, many=True)
        return Response(serializer.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        This method needs for handle all http POST requests on permission-list and add new permission for user

        :param request: http request
        :param args: other  parameters
        :param kwargs: dict parsed url variables {repository_id:id}
        :return: json with new permissions
        :raise Validations error from serializer
        """
        serializer_context = {
            'request': Request(request),
            'repository_id': kwargs['repository_id'],
        }
        serializer = PermissionSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionDetail(APIView):
    """
    This view handle all requests what comes on endpoint repositories/(?P<repository_id>[0-9]+)/permissions/(?P<permission_id>[0-9]+)/$
    """

    serializer_class = PermissionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, request, *args, **kwargs):
        """
        Trying to get permission(permission and repository id) in database and return them

        :param args: other parameters
        :param kwargs: dict parsed url variables {"permission_id": "id", "repository_id":"id"}
        :return: UserPermissions object or DoesNotExist exception
        :raise UserPermissions.DoesNotExist
        """
        try:
            permission = UserPermissions.objects.get(id=kwargs['permission_id'],
                                                     repository_id=kwargs['repository_id'])
        except UserPermissions.DoesNotExist:
            raise Http404

        super(PermissionDetail, self).check_permissions(request)
        return permission

    def get(self, request: Request, *args, **kwargs: dict) -> Response:
        """
        This method handle GET request return JSON with detailed information for specific permission

        :param request: http request
        :param args: other parameters
        :param kwargs: dict parsed url variables {"permission_id": "id", "repository_id":"id"}
        :return: HTTP response with serialized in JSON permission data
        """
        permission = self.get_object(request, **kwargs)
        serializer_context = {
            'request': Request(request),
            'repository_id': kwargs['repository_id'],
        }
        serializer = PermissionSerializer(permission, context=serializer_context)
        return Response(serializer.data)

    def delete(self, request: Request, *args, **kwargs: dict) -> Response:
        """
        This method handle DELETE http request on permission detail endpoint

        :param request: http request
        :param args: other parameters
        :param kwargs: dict parsed url variables {"permission_id": "id", "repository_id":"id"}
        :return: on success HTTP 204 status code, else return 404
        """
        permission = self.get_object(request, **kwargs)
        super(PermissionDetail, self).check_object_permissions(request, permission)
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
