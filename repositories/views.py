import base64
import json
import logging
import os
import secrets
import struct

from django.http import Http404
from django.utils import timezone
from django.utils.datetime_safe import datetime
from rest_framework import status, filters
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from branches.models import Branch
from commits.models import Commit
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
# @permission_required([IsContributorOrReadOnly, IsOwnerOrReadOnly])
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


    json_content = json.loads(request.body)
    try:
        repo = Repository.objects.get(pk=kwargs['repository_id'])
    except Repository.DoesNotExist:
        raise Http404

    comment_diff = []
    if Branch.objects.filter(name=json_content['branch_name']).exists():
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
# @permission_required([IsContributorOrReadOnly, IsOwnerOrReadOnly])
def push_add_commits(request: Request, *args, **kwargs) -> Response:
    raw_request = json.loads(json.loads(request.body))

    # print(type(raw_request))
    # print(raw_request)
    # print( raw_request['data'].encode())
    decoded_request = base64.decodebytes(raw_request['data'].encode())
    # print(type(decoded_request))
    curr_size = 8
    size_of_package = struct.unpack('Q', decoded_request[:8])[0]

    package_content = json.loads(decoded_request[curr_size:size_of_package + 8].decode('utf-8'))
    curr_size = size_of_package
    log_size = int(package_content['logs'])

    curr_path = '/home/dimasik/lit-be'
    repo_path = curr_path + '/' + kwargs['repository_id']
    if (os.path.exists(repo_path)):
        os.chdir(repo_path)
    else:
        os.mkdir(repo_path)

    with open('commits_log.json', 'w') as commit_log:
        commit_log.write(decoded_request[curr_size + 8:curr_size + log_size + 8].decode('utf-8'))

        commits_log_list = json.loads(decoded_request[curr_size + 8:curr_size + log_size + 8].decode('utf-8'))
        commit_log.close()
    # test = open('commits_log.json')
    #

    count_commits = int(Commit.objects.all().count())
    for commit in commits_log_list:
        branch = Branch.objects.get(name=raw_request['branch_name'])
        commit_time = timezone.make_aware(
            datetime.strptime(commit['datetime'], '%Y-%m-%d %H:%M:%S.%f'), timezone.get_fixed_timezone(0))

        commit_to_save = Commit(id=count_commits + 1,
                                user=User.objects.get(username=commit['user']),
                                long_hash=commit['long_hash'],
                                branch=(branch,),
                                commit_time=commit_time,
                                comment=commit['message'])
        commit_to_save.save()

    # print(log_size)
    # print(curr_size)
    curr_size += log_size

    for commit in package_content['commits']:
        commit_key = list(commit.keys())[0]
        with open(commit_key + '.zip', 'wb') as commit_zip:
            commit_zip.write(decoded_request[curr_size:curr_size + int(commit[commit_key])])
            curr_size += int(commit[commit_key])
            commit_zip.close()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def pull(request, repository_id):
    json_content = json.loads(request.body.decode())
    # print(json_content)
    repo_id = json_content['repo_id']
    branch_name = json_content['branch_name']
    commits_on_cli = json_content['commits_hashes']
    commit_diff = []
    curr_path = '/home/dimasik/lit-be'

    for commit in Commit.objects.filter(branch=Branch.objects.filter(name=branch_name, repository=repo_id)):
        if commit.long_hash not in commits_on_cli and commit.long_hash not in commit_diff:
            commit_diff.append(commit.long_hash)

    repo_path = curr_path + '/' + str(repo_id)
    if (os.path.exists(repo_path)):
        os.chdir(repo_path)
    else:
        os.mkdir(repo_path)

    # commits_logs = json.load(open('commits_log.json')).encode()
    # commits_logs_bytes = json.dumps(commits_logs)
    # print(os.getcwd())

    with open('commits_log.json') as commits_logs:
        content = commits_logs.read()
        commits_logs = json.loads(content)

    commits_logs_bytes = json.dumps(commits_logs).encode('utf-8')
    commits_archives_bytes = bytearray()
    archives_lengths = {}
    #print('Commmit_diff')
   # print(commit_diff)

    for commit_hash in commit_diff:
        archive_name = commit_hash[:] + '.zip'
        archive_path = os.path.join(repo_path, archive_name)
        with open(archive_path, 'rb') as archive_file:
            file_bytes = archive_file.read()
            archives_lengths[commit_hash] = len(file_bytes)
            commits_archives_bytes.extend(file_bytes)
           # print('added archive {0}'.format(archive_path))


    memory_map = {'logs': len(commits_logs_bytes), 'commits': list()}
    for k, v in archives_lengths.items():
        memory_map['commits'].append({k: v})
    memory_map_bytes = json.dumps(memory_map).encode('utf-8')


    # print(commits_logs_bytes)
    # print(type(commits_logs_bytes))
    package_bytes = bytearray()
    package_bytes.extend(struct.pack('Q', len(memory_map_bytes)))
    package_bytes.extend(memory_map_bytes)
    package_bytes.extend(commits_logs_bytes)
    package_bytes.extend(commits_archives_bytes)

    return Response(data=base64.b64encode(package_bytes), status=status.HTTP_200_OK)
