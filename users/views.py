import logging

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserList(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer_context = {
            'request': Request(request),
        }
        serializer = UserSerializer(users, context=serializer_context, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_context = {
            'request': Request(request),
        }
        serializer = UserSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist as e:
            logger.exception(e)
            raise Http404

    def get(self, request, *args, **kwargs):
        user = self.get_object(kwargs['user_id'])
        serializer_context = {
            'request': Request(request),
        }
        serializer = UserSerializer(user, context=serializer_context)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = self.get_object(kwargs['user_id'])
        serializer_context = {
            'request': Request(request),
        }
        serializer = UserSerializer(user, data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.get_object(kwargs['user_id'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
