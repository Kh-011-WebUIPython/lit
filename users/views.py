import logging

from django.http import Http404, HttpResponse
from rest_auth.views import UserDetailsView
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions.models import UserPermissions, PERMISSIONS
from users.models import User
from users.serializers import UserSerializer, UserRepositorySerializer

logger = logging.getLogger(__name__)


class HackedUserDetailsView(UserDetailsView):
    """
    Special hack to return 200 for `options` requests
    """
    def check_permissions(self, request):
        if request.method.lower() in ['options']:
            return  # to skip raising an exception
        return super(UserDetailsView, self).check_permissions(request)

    def options(self, request, *args, **kwargs):
        return HttpResponse(status=200)


class UserList(ListCreateAPIView):
    """
    View for handle GET and POST methods on user entity with search fields(username, email)

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$username', '=email')
    parser_classes = (MultiPartParser,)


class UserRepositoryList(ListAPIView):
    """
    View for handle GET requests on user-repositories endpoint and return user permissions to specific repository
    """
    serializer_class = UserRepositorySerializer

    def get_queryset(self):
        queryset = UserPermissions.objects.filter(user_id=self.kwargs['user_id'])
        status = self.request.query_params.get('status', None)
        flag = True
        if status is not None:
            for short_permission, long_permission in PERMISSIONS:
                if status in (short_permission, long_permission):
                    status = short_permission
                    flag = False
                    break
            if flag:
                raise Http404
            queryset = queryset.filter(status=status)
        return queryset


class UserDetail(APIView):
    """
    This view handle all requests what comes on endpoint /users/(?P<user_id>[0-9]+)$
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    parser_classes = (MultiPartParser,)

    @staticmethod
    def get_object(user_id: int) -> User:
        """
        Trying to find user by ID in database and return them

        :param user_id: user id
        :return: User object or DoesNotExist exception
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            logger.exception(e)
            raise Http404

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        This method handle GET request on base view url and return JSON with user data

        :param request: http request
        :param args: other parameters
        :param kwargs: dict parsed url variables {"user_id": "id"}
        :return: HTTP response with serialized in JSON user data
        """
        user = self.get_object(kwargs['user_id'])
        serializer = UserSerializer(user, context={'request': Request(request)})
        return Response(serializer.data)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        This method handle PUT request on base view url and return updated JSON user data

        :param request: http request
        :param args: other parameters
        :param kwargs: dict parsed url variables {"user_id": "id"}
        :return: updated JSON user data or HTTP status code 400
        """
        user = self.get_object(kwargs['user_id'])
        serializer = UserSerializer(user, data=request.data, context={'request': Request(request)})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        This method handle DELETE http request on user detail endpoint

        :param request: http request
        :param args:  other parameters
        :param kwargs: dict parsed url variables {"user_id": "id"}
        :return: on success HTTP 204 status code, else return 404
        """
        user = self.get_object(kwargs['user_id'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
