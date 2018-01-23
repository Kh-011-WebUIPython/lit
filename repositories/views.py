import json
import logging
import os
import struct

from django.http import Http404
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from lit.permissions import IsOwnerOrReadOnly
from repositories.models import Repository
from repositories.serializers import RepositorySerializer

logger = logging.getLogger(__name__)


class RepositoryList(ListCreateAPIView):
    """
    View for handle GET and POST methods on repository endpoint
    """
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description',)


class RepositoryDetail(APIView):
    """
    View for handle main http methods(GET,PUT,DELETE) on repository entity
    URL --> /repositories/(?P<repository_id>[0-9]+)$
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, request, repository_id: int) -> Repository:
        """
        Find repository by repository ID in DB

        :param repository_id: parameter from this url--> /repositories/(?P<repository_id>[0-9]+)$
        :return: Repository or rise exception HTTP_404
        """
        try:
            repo = Repository.objects.get(pk=repository_id)
        except Repository.DoesNotExist:
            raise Http404
        super(RepositoryDetail, self).check_permissions(request)
        return repo

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Method for handle GET request on /repositories/{repository_id}

        :param request: incoming http request
        :param args: other parameters
        :param kwargs: dict parsed url variables {"repository_id": "id"}
        :return: JSON data with specific repository
        """
        repo = self.get_object(request, kwargs['repository_id'])
        serializer = RepositorySerializer(repo, context={'request': Request(request)})
        return Response(serializer.data)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Method for handle HTTP PUT request on /repositories/{repository_id}

        :param request: incoming http request
        :param args: other parameters
        :param kwargs: dict parsed url variables {"repository_id": "id"}
        :return: JSON data with specific repository, else return 400 and reason why that's happen
        """
        repo = self.get_object(request, kwargs['repository_id'])
        super(RepositoryDetail, self).check_object_permissions(request, repo)
        serializer = RepositorySerializer(repo, data=request.data, context={'request': Request(request)})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Method for handle HTTP DELETE request on /repositories/{repository_id}

        :param request: incoming http request
        :param args: other parameters
        :param kwargs: dict parsed url variables {"repository_id": "id"}
        :return: On success HTTP 204 status code, else return 404
        """
        repo = self.get_object(request, kwargs['repository_id'])
        super(RepositoryDetail, self).check_object_permissions(request, repo)
        repo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        # TODO check this method because it prototype


@api_view(['POST'])
def push(request: Request, *args, **kwargs) -> Response:
    """
    Method for handle POST(push) request on /repositories/{repository_id}
    :param request: incoming http request
    :param args: other parameters
    :param kwargs: dict parsed url variables {"repository_id": "id"}
    :return: on success HTTP 200 status code, else 404
    """

    size_of_package = struct.unpack('Q', request.body[:8])[0]
    curr_size = size_of_package
    package_content = json.loads(request.body[8:curr_size].decode('utf-8'))
    log_size = int(package_content['logs'])

    curr_path = os.getcwd()
    repo_path = curr_path + '/' + kwargs['repository_id']
    os.mkdir(repo_path)
    os.chdir(repo_path)

    with open('commits_log.json', 'w') as commit_log:
        commit_log.write(request.body[curr_size:curr_size + log_size].decode('utf-8'))
        commit_log.close()

    curr_size += log_size

    for key, value in package_content['commits'][0].items():
        with open(key + '.zip', 'w') as commit_zip:
            commit_zip.write(request.body[curr_size:curr_size + int(value)].decode('utf-8'))
            curr_size += int(value)
            commit_zip.close()

    os.chdir(curr_path)
    return Response(status=status.HTTP_200_OK)
