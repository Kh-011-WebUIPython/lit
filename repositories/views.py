import logging

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from lit.permissions import IsOwnerOrReadOnly
from repositories.models import Repository
from repositories.serializers import RepositorySerializer

logger = logging.getLogger(__name__)


class RepositoryList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        repos = Repository.objects.all()
        serializer_context = {
            'request': Request(request),
        }
        serializer = RepositorySerializer(repos, context=serializer_context, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_context = {
            'request': Request(request),
        }
        serializer = RepositorySerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RepositoryDetail(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Repository.objects.get(pk=pk)
        except Repository.DoesNotExist as e:
            logger.exception(e)
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        repo = self.get_object(pk)
        serializer_context = {
            'request': Request(request),
        }
        serializer = RepositorySerializer(repo, context=serializer_context)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        repo = self.get_object(pk)
        serializer_context = {
            'request': Request(request),
        }
        serializer = RepositorySerializer(repo, data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        repo = self.get_object(pk)
        repo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
