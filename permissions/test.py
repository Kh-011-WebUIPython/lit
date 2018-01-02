from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase

from permissions.models import UserPermissions, PERM_CONTRIB, PERM_OWNER
from repositories.models import Repository
from users.models import User


class TestPermissionsApi(APITestCase):
    def setUp(self):
        self.user_dimasik = User(username='dimasik', email='dimasik@gmail.com', password='dimasdimas')
        self.user_dimason = User(username='dimason', email='dimason@gmail.com', password='dimasdimas')
        self.user_dimas = User(username='dimas', email='dimas@gmail.com', password='dimasdimas')
        self.user_dimasik.save()
        self.user_dimason.save()
        self.user_dimas.save()

        self.repository = Repository(name='DimasikRepo', description='Test permission for this repository')
        self.repository.save()

        self.permissions_dimasik = UserPermissions(user=self.user_dimasik, repository=self.repository,
                                                   status=PERM_OWNER)
        self.permissions_dimason = UserPermissions(user=self.user_dimason, repository=self.repository,
                                                   status=PERM_CONTRIB)
        self.permissions_dimasik.save()
        self.permissions_dimason.save()

    def test_get_permissions_list(self):
        """
        Test case for get all permissions from repository
        """
        client_owner = APIClient()
        client_owner.force_authenticate(user=self.user_dimasik)
        response = client_owner.get(
            reverse('permissions:permission-list', kwargs={'repository_id': 1}))

        self.assertEqual(UserPermissions.objects.count(), 2)
        self.assertEqual(response.status_code, 200)

    def test_get_permission(self):
        """
        Test case for get one permission from repository
        """
        client_owner = APIClient()
        client_owner.force_authenticate(user=self.user_dimasik)
        response = client_owner.get(
            reverse('permissions:permission-detail', kwargs={'repository_id': 1, 'permission_id': 1}), format='json')
        # TODO get to know what it response
        self.assertEqual(response.status_code, 200)

    def test_delete_permission(self):
        """
        Test case for delete permission from repository
        We can delete owner permission?
        """
        client_owner = APIClient()
        client_owner.force_authenticate(user=self.user_dimasik)
        response = client_owner.delete(
            reverse('permissions:permission-detail', kwargs={'repository_id': 1, 'permission_id': 1}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(UserPermissions.objects.count(), 1)

    def test_delete_repository_contributor(self):
        """
        Test case for contributor delete repository
        Contributor can delete repo?
        """
        client_contributor = APIClient()
        client_contributor.force_authenticate(user=self.user_dimason)
        response = client_contributor.delete(reverse('repositories:repository-detail', kwargs={'repository_id': 1}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Repository.objects.count(), 1)

    def test_create_permission(self):
        """
        Test case for create permission
        """
        # TODO get to know how create permission
        client = APIClient()
        client.force_authenticate(user=self.user_dimas)
        response = client.post(reverse('permissions:permission-list',
                                       kwargs={'repository_id': 1,
                                               'username': self.user_dimas.username}), format='json')
        self.assertEqual(response.status_code, 201)
