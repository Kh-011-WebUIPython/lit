import base64
import json
import logging
import os
import struct

from django.http import Http404
from rest_framework import status, filters
from rest_framework.decorators import api_view
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
    Method for handle POST request on /repositories/{repository_id}/push
    :param request: incoming http request
    :param args: other parameters
    :param kwargs: dict parsed url variables {"repository_id": "id"}
    :return: on success HTTP 200 status code, else 404
    """
    decoded_request = base64.decodebytes(request)
    curr_size = 8
    size_of_package = struct.unpack('Q', decoded_request[:8])[0]

    package_content = json.loads(decoded_request[curr_size:size_of_package+8].decode('utf-8'))
    curr_size = size_of_package
    log_size = int(package_content['logs'])

    curr_path = os.getcwd()
    repo_path = curr_path + '/' + kwargs['repository_id']
    os.mkdir(repo_path)
    os.chdir(repo_path)

    with open('commits_log.json', 'w') as commit_log:
        commit_log.write( decoded_request[curr_size:curr_size + log_size].decode('utf-8'))
        commit_log.close()

    curr_size += log_size

    for commit in package_content['commits']:
        with open(list(commit.keys())[0] + '.zip', 'wb') as commit_zip:
            commit_zip.write(decoded_request[curr_size:curr_size + int(commit[list(commit.keys())[0]])])
            curr_size += int(commit[list(commit.keys())[0]])
            commit_zip.close()

    os.chdir(curr_path)
    return Response(status=status.HTTP_200_OK)
