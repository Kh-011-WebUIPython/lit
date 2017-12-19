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
