from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase

from branches.models import Branch
from permissions.models import UserPermissions, PERM_CONTRIB, PERM_OWNER
from repositories.models import Repository
from users.models import User

class TestBranchApi(APITestCase):
    def setUp(self):
        self.user_dimasik = User(username='dimasik', email='dimasik@gmail.com', password='dimasdimas')
        self.user_dimason = User(username='dimason', email='dimason@gmail.com', password='dimasdimas')
        self.user_dimas = User(username='dimas', email='dimas@gmail.com', password='dimasdimas')
        self.user_dimasik.save()
        self.user_dimason.save()
        self.user_dimas.save()

        self.repository = Repository(name='DimasikRepo', description='Test branches for this repository')
        self.repository.save()

        self.permissions_dimasik = UserPermissions(user=self.user_dimasik, repository=self.repository,
                                                   status=PERM_OWNER)
        self.permissions_dimason = UserPermissions(user=self.user_dimason, repository=self.repository,
                                                   status=PERM_CONTRIB)
        self.permissions_dimasik.save()
        self.permissions_dimason.save()

        self.branch1 = Branch(name='branch1', repository=self.repository)
        self.branch2 = Branch(name='branch2', repository=self.repository)
        self.branch3 = Branch(name='branch3', repository=self.repository)
        self.branch4 = Branch(name='branch4', repository=self.repository)
        self.branch1.save()
        self.branch2.save()
        self.branch3.save()
        self.branch4.save()

    def test_get_branch_list(self):
        """
        Test case for get all branches from repository
        """
        client_owner = APIClient()
        client_owner.force_authenticate(user=self.user_dimasik)
        response = client_owner.get(
            reverse('branches:branch-list', kwargs={'repository_id': 1}))

        self.assertEqual(Branch.objects.count(), 4)
        self.assertEqual(response.status_code, 200)

    def test_get_branch(self):
        """
        Test case for get one branch from repository
        """
        client_owner = APIClient()
        client_owner.force_authenticate(user=self.user_dimasik)
        response = client_owner.get(
            reverse('branches:branch-detail', kwargs={'branch_id': 1, 'repository_id': 1}), format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_branch_owner(self):
        """
        Test case for delete branch from repository
        """
        client_owner = APIClient()
        client_owner.force_authenticate(user=self.user_dimasik)
        response = client_owner.delete(
            reverse('branches:branch-detail', kwargs={'branch_id': 1, 'repository_id': 1}), format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Branch.objects.count(), 3)

    def test_create_branch_noname(self):
        """
        Test case for create branch from anonymous
        """
        client = APIClient()
        client.force_authenticate(user=self.user_dimas)
        response = client.post(reverse('branches:branch-list', kwargs={'repository_id': 1}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Branch.objects.count(), 4)

    def test_create_branch_contributor(self):
        """
        Test case for create branch from contributor
        """
        client_contrib = APIClient()
        client_contrib.force_authenticate(user=self.user_dimason)
        response = client_contrib.post(reverse('branches:branch-list', kwargs={'repository_id': 1}))
        self.assertEqual(response.status_code, 400)

    def test_create_branch_owner(self):
        """
        Test case for create branch from owner
        """
        client_owner = APIClient()
        client_owner.force_authenticate(user=self.user_dimasik)
        response = client_owner.post(reverse('branches:branch-list', kwargs={'repository_id': 1}))
        self.assertEqual(response.status_code, 400)
