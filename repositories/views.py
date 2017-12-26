import logging

from django.http import Http404
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from lit.permissions import IsOwnerOrReadOnly
from repositories.models import Repository
from repositories.serializers import RepositorySerializer

logger = logging.getLogger(__name__)


class RepositoryList(ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description',)


class RepositoryDetail(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, rpk):
        try:
            return Repository.objects.get(pk=rpk)
        except Repository.DoesNotExist as e:
            logger.exception(e)
            raise Http404

    def get(self, request, *args, **kwargs):
        repo = self.get_object(kwargs['repository_id'])
        serializer_context = {
            'request': Request(request),
        }
        serializer = RepositorySerializer(repo, context=serializer_context)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        repo = self.get_object(kwargs['repository_id'])
        serializer_context = {
            'request': Request(request),
        }
        serializer = RepositorySerializer(repo, data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        repo = self.get_object(kwargs['repository_id'])
        repo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
