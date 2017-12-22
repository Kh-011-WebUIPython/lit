import logging

from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from commits.serializers import CommitSerializer
from commits.models import Commit

logger = logging.getLogger(__name__)


class CommitList(APIView):


    def get(self, request, *args, **kwargs):
        commits = Commit.objects.all()
        serializer_context = {
            'request': Request(request)
        }
        serializer = CommitSerializer(commits, context = serializer_context, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_context = {
            'request': Request(request),
        }
        serializer = CommitSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommitDetail(APIView):


    def get_object(self, pk):
        try:
            return Commit.objects.get(pk=pk)
        except Commit.DoesNotExist as e:
            logger.exception(e)
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        commit = self.get_object(pk)
        serializer_context = {
            'request': Request(request),
        }
        serializer = CommitSerializer(commit, context=serializer_context)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        commit = self.get_object(pk)
        serializer_context = {
            'request': Request(request),
        }
        serializer = CommitSerializer(commit, data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        commit = self.get_object(pk)
        commit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)