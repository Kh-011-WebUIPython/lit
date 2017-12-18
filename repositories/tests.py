import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from permissions.models import UserPermissions, PERM_OWNER
from repositories.models import Repository
from users.models import User


class TestRepositoryApi(APITestCase):

    def setUp(self):
        self.repository = Repository(name='Project-basic')
        self.repository.save()

        self.user1 = User(username='user1', email='users1@litvcs.win', password='}{qwerty}{')
        self.user1.save()

        up = UserPermissions(user=self.user1, repository=self.repository, status=PERM_OWNER)
        up.save()

        self.user2 = User(username='user2', email='users2@litvcs.win', password='}{qwerty}{')
        self.user2.save()

    def test_create_repository(self):
        """
        Test case for create a repository
        """
        client = APIClient()
        client.force_authenticate(user=self.user1)
        url = reverse('repositories:repository-list')
        data = {'name': 'Project1', 'created': datetime.datetime.now()}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Repository.objects.count(), 2)
        self.assertEqual(Repository.objects.get(id=2).name, 'Project1')
        self.assertEqual(UserPermissions.objects.get(repository=Repository.objects.get(id=2),
                                                     user=self.user1).status, PERM_OWNER)

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
        url = reverse('repositories:repository-detail', kwargs={'rpk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.json()['name'], 'Project-basic')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(Repository.objects.get().name, 'Project-basic')

    def test_put_repository_unauthorized_fail(self):
        """
        Test case for update a repository
        """
        url = reverse('repositories:repository-detail', kwargs={'rpk': 1})
        data = {'name': 'Project2'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_repository(self):
        """
        Test case for update a repository
        """
        url = reverse('repositories:repository-detail', kwargs={'rpk': 1})
        data = {'name': 'Project2', 'created': datetime.datetime.now()}

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.put(url, data, format='json')

        self.assertEqual(response.json()['name'], 'Project2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(Repository.objects.get().name, 'Project2')

    def test_delete_repository(self):
        """
        Test case for delete a repository
        """
        url = reverse('repositories:repository-detail', kwargs={'rpk': 1})
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Repository.objects.count(), 0)

    def test_delete_repository_unauthorized_fail(self):
        """
        Test case for delete a repository
        """
        url = reverse('repositories:repository-detail', kwargs={'rpk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Repository.objects.count(), 1)
