import logging

from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from branches.models import Branch
from branches.serializers import BranchSerializer
from lit.permissions import IsContributorOrReadOnly, IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


class BranchList(APIView):
    permission_classes = (IsContributorOrReadOnly, IsOwnerOrReadOnly,)

    def get(self, request, rpk, *args, **kwargs):
        branches = Branch.objects.filter(repository_id=rpk)
        serializer_context = {
            'request': Request(request),
        }
        serializer = BranchSerializer(branches, context=serializer_context, many=True)
        return Response(serializer.data)

    def post(self, request, rpk, *args, **kwargs):
        serializer_context = {
            'request': Request(request),
            'repository_id': rpk,
        }
        serializer = BranchSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchDetail(APIView):
    permission_classes = (IsContributorOrReadOnly, IsOwnerOrReadOnly,)

    def get_object(self, bpk, rpk):
        try:
            return Branch.objects.get(id=bpk,
                                      repository_id=rpk)
        except Branch.DoesNotExist as e:
            logger.exception(e)
            raise Http404

    def get(self, request, bpk, rpk, *args, **kwargs):
        branch = self.get_object(bpk=bpk, rpk=rpk)
        serializer_context = {
            'request': Request(request),
        }
        serializer = BranchSerializer(branch, context=serializer_context)
        return Response(serializer.data)

    def delete(self, request, bpk, *args, **kwargs):
        branch = self.get_object(bpk)
        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
