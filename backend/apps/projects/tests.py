from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apps.organizations.models import Organization
from apps.user_profiles.models import Profile
from apps.workspaces.models import Workspace
from .models import Project, ProjectMember


User = get_user_model()


class ProjectApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.organization = Organization.objects.create(name='Org A')
        self.workspace = Workspace.objects.create(name='Workspace A', organization=self.organization)
        self.other_workspace = Workspace.objects.create(name='Workspace B', organization=self.organization)

        self.user = User.objects.create_user(username='user1', email='user1@example.com', password='StrongPass123!')
        Profile.objects.create(user=self.user, workspace=self.workspace)

        self.other_user = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='StrongPass123!',
        )
        Profile.objects.create(user=self.other_user, workspace=self.other_workspace)

        self.client.force_authenticate(user=self.user)

    def test_create_project_creates_owner_membership(self):
        response = self.client.post(
            '/api/v1/projects/',
            {'name': 'Alpha', 'description': 'Desc', 'status': 'active'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(name='Alpha')
        self.assertEqual(project.workspace, self.workspace)
        self.assertEqual(project.created_by, self.user)
        self.assertTrue(ProjectMember.objects.filter(project=project, user=self.user).exists())

    def test_user_sees_only_own_workspace_projects(self):
        own_project = Project.objects.create(
            workspace=self.workspace,
            name='Own Project',
            created_by=self.user,
        )
        ProjectMember.objects.create(project=own_project, user=self.user, role=ProjectMember.Role.OWNER)

        other_project = Project.objects.create(
            workspace=self.other_workspace,
            name='Other Project',
            created_by=self.other_user,
        )
        ProjectMember.objects.create(project=other_project, user=self.other_user, role=ProjectMember.Role.OWNER)

        response = self.client.get('/api/v1/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item['id'] for item in response.data['results']}
        self.assertIn(own_project.id, returned_ids)
        self.assertNotIn(other_project.id, returned_ids)

    def test_filter_search_and_ordering(self):
        first = Project.objects.create(
            workspace=self.workspace,
            name='Alpha',
            description='First project',
            status='active',
            created_by=self.user,
        )
        second = Project.objects.create(
            workspace=self.workspace,
            name='Beta',
            description='Second project',
            status='planning',
            created_by=self.user,
        )
        ProjectMember.objects.create(project=first, user=self.user, role=ProjectMember.Role.OWNER)
        ProjectMember.objects.create(project=second, user=self.user, role=ProjectMember.Role.OWNER)

        filtered = self.client.get('/api/v1/projects/?status=active')
        self.assertEqual(filtered.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filtered.data['results']), 1)
        self.assertEqual(filtered.data['results'][0]['id'], first.id)

        searched = self.client.get('/api/v1/projects/?search=second')
        self.assertEqual(searched.status_code, status.HTTP_200_OK)
        self.assertEqual(len(searched.data['results']), 1)
        self.assertEqual(searched.data['results'][0]['id'], second.id)

        ordered = self.client.get('/api/v1/projects/?ordering=name')
        self.assertEqual(ordered.status_code, status.HTTP_200_OK)
        self.assertEqual(ordered.data['results'][0]['name'], 'Alpha')

    def test_jwt_authentication_required(self):
        self.client.force_authenticate(user=None)
        unauthenticated = self.client.get('/api/v1/projects/')
        self.assertEqual(unauthenticated.status_code, status.HTTP_401_UNAUTHORIZED)

        token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        authenticated = self.client.get('/api/v1/projects/')
        self.assertEqual(authenticated.status_code, status.HTTP_200_OK)
