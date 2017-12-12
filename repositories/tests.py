import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from repositories.models import Repository


class TestRepositoryApi(APITestCase):
    def setUp(self):
        self.repository = Repository(name='Project-basic')
        self.repository.save()

    def test_create_repository(self):
        """
        Test case for create a repository
        """
        url = reverse('repositories:repository-list')
        data = {'name': 'Project1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Repository.objects.count(), 2)
        self.assertEqual(Repository.objects.get(id=2).name, 'Project1')

    def test_list_repositories(self):
        """
        Test case for get all repository
        """
        url = reverse('repositories:repository-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(Repository.objects.get().name, 'Project-basic')

    def test_get_repository(self):
        """
        Test case for get a repository
        """
        url = reverse('repositories:repository-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(json.loads(response.content)['name'], 'Project-basic')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(Repository.objects.get().name, 'Project-basic')

    def test_put_repository(self):
        """
        Test case for update a repository
        """
        url = reverse('repositories:repository-detail', kwargs={'pk': 1})
        data = {'name': 'Project2'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(json.loads(response.content)['name'], 'Project2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(Repository.objects.get().name, 'Project2')

    def test_delete_repository(self):
        """
        Test case for delete a repository
        """
        url = reverse('repositories:repository-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Repository.objects.count(), 0)

