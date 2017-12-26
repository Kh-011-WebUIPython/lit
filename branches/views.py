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
    """
    Basic view for handle all http requests to branch-list endpoint

    """
    permission_classes = (IsContributorOrReadOnly, IsOwnerOrReadOnly,)

    def get(self, request:Request, *args, **kwargs) -> Response:
        """
        This method needs for handle GET request on branch-list endpoint and return all branches for specific repository

        :param request: http request
        :param args: other  parameters
        :param kwargs: dict parsed url variables {repository_id:id}
        :return: json with all branches for repository
        """

        branches = Branch.objects.filter(repository_id=kwargs['repository_id'])
        serializer = BranchSerializer(branches, context={'request': Request(request)}, many=True)
        return Response(serializer.data)

    def post(self, request:Request, *args, **kwargs) -> Response:
        """
        This method needs for handle all http POST requests on branch-list and create new branches for specific repository

        :param request: http request
        :param args: other  parameters
        :param kwargs: dict parsed url variables {repository_id:id}
        :return: json with new branch
        """

        serializer_context = {
            'request': Request(request),
            'repository_id': kwargs['repository_id'],
        }
        serializer = BranchSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchDetail(APIView):
    """
    This view handle all requests what comes on endpoint repositories/(?P<repository_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/$

    """
    permission_classes = (IsContributorOrReadOnly, IsOwnerOrReadOnly,)

    @staticmethod
    def get_object(*args, **kwargs) -> Branch:
        """
        Trying to find branch by branch and repository id in database and return them

        :param args: other parameters
        :param kwargs: dict parsed url variables {"branch_id": "id", "repository_id":"id"}
        :return: Branch object or DoesNotExist exception
        :raise Branch.DoesNotExist
        """

        try:
            return Branch.objects.get(id=kwargs['branch_id'],
                                      repository_id=kwargs['repository_id'])
        except Branch.DoesNotExist as e:
            logger.exception(e)
            raise Http404

    def get(self, request:Request, *args, **kwargs) -> Response:
        """
        This method handle GET request return JSON with information for specific branch

        :param request: http request
        :param args: other parameters
        :param kwargs: dict parsed url variables {"branch_id": "id", "repository_id":"id"}
        :return: HTTP response with serialized in JSON branch data
        """

        branch = self.get_object(branch_id=kwargs['branch_id'], repository_id=kwargs['repository_id'])
        serializer_context = {
            'request': Request(request),
            'repository_id': kwargs['repository_id'],
        }
        serializer = BranchSerializer(branch, context=serializer_context)
        return Response(serializer.data)

    def delete(self, request:Request, *args, **kwargs) -> Response:
        """
        This method handle DELETE http request on branch-detail endpoint

        :param request: http request
        :param args:  other parameters
        :param kwargs: dict parsed url variables {"branch_id": "id"}
        :return: on success HTTP 204 status code, else return 404
        """

        branch = self.get_object(kwargs['branch_id'])
        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
