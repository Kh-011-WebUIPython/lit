import base64
import json
import logging
import os
import secrets
import struct
from pprint import pprint

from django.contrib.auth.decorators import permission_required
from django.http import Http404
from rest_framework import status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from branches.models import Branch
from commits.models import Commit
from lit.permissions import IsContributorOrReadOnly
from lit.permissions import IsOwnerOrReadOnly
from repositories.models import Repository
from repositories.serializers import RepositorySerializer
from users.models import User

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
#@permission_required([IsContributorOrReadOnly, IsOwnerOrReadOnly])
def push_check_commits(request: Request, *args, **kwargs) -> Response:
    """
    Method for handle POST request on /repositories/{repository_id}/push
    :param request: incoming http request
    :param args: other parameters
    :param kwargs: dict parsed url variables {"repository_id": "id"}
    :return: on success HTTP 200 status code, else 404
    """
    # TODO check for permissions
    # Phase 1

    print(request.user)

    json_content = json.loads(request.body)
    try:
        repo = Repository.objects.get(pk=kwargs['repository_id'])
    except Repository.DoesNotExist:
        raise Http404

    comment_diff = []
    if  Branch.objects.filter(name=json_content['branch_name']).exists():
        for commit_hash in json_content['commits_hashes']:
            if (commit_hash not in Commit.objects.all()):
                comment_diff.append(commit_hash)
    else:
        branch = Branch(name=json_content['branch_name'], repository=repo)
        branch.save()
        comment_diff = json_content['commits_hashes'][:]

    response = {"session_token": secrets.token_hex(16), "commits": comment_diff}
    return Response(response, status=status.HTTP_200_OK)


# Phase 2
# TODO check this method because it prototype
@api_view(['POST'])
#@permission_required([IsContributorOrReadOnly, IsOwnerOrReadOnly])
def push_add_commits(request: Request, *args, **kwargs) -> Response:

    raw_request = json.loads(json.loads(request.body))

    #print(type(raw_request))
    #print(raw_request)
    #print( raw_request['data'].encode())
    decoded_request = base64.decodebytes(raw_request['data'].encode())
    #print(type(decoded_request))
    curr_size = 8
    size_of_package = struct.unpack('Q', decoded_request[:8])[0]

    package_content = json.loads(decoded_request[curr_size:size_of_package + 8].decode('utf-8'))
    curr_size = size_of_package
    log_size = int(package_content['logs'])

    curr_path = os.getcwd()

    repo_path = curr_path + '/' + kwargs['repository_id']
    os.mkdir(repo_path)
    os.chdir(repo_path)

    with open('commits_log.json', 'w') as commit_log:
        commit_log.write(decoded_request[curr_size + 8:curr_size + log_size + 8].decode('utf-8'))

        commits_log_dict = json.loads(decoded_request[curr_size + 8:curr_size + log_size + 8].decode('utf-8'))
        commit_log.close()
    # test = open('commits_log.json')
    #
    # for commit in commits_log_dict:
    #     commit_to_save = Commit(user=User.objects.get(username=commit['user']),
    #                             long_hash=commit['long_hash'],
    #                             branch=Branch.objects.filter(name=raw_request['branch_name']).first().id,
    #                             commit_time=commit['datetime'],
    #                             comment=commit['message'])
    #     commit_to_save.save(commit=False)
    #     commit.save_m2m()
    # print(log_size)
    # print(curr_size)
    curr_size += log_size

    for commit in package_content['commits']:
        commit_key = list(commit.keys())[0]
        with open(commit_key + '.zip', 'wb') as commit_zip:
            commit_zip.write(decoded_request[curr_size:curr_size + int(commit[commit_key])])
            curr_size += int(commit[commit_key])
            commit_zip.close()

    os.chdir(curr_path)
    return Response(status=status.HTTP_200_OK)
