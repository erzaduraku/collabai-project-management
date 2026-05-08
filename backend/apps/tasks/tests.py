from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.organizations.models import Organization
from apps.projects.models import Project, ProjectMember
from apps.user_profiles.models import Profile
from apps.workspaces.models import Workspace
from .models import Task, TaskStatus


User = get_user_model()


class TaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        organization = Organization.objects.create(name='Tasks Org')
        self.workspace = Workspace.objects.create(name='Tasks WS', organization=organization)
        self.other_workspace = Workspace.objects.create(name='Other WS', organization=organization)

        self.user = User.objects.create_user(username='tasker', email='tasker@example.com', password='StrongPass123!')
        Profile.objects.create(user=self.user, workspace=self.workspace)

        self.other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='StrongPass123!',
        )
        Profile.objects.create(user=self.other_user, workspace=self.other_workspace)

        self.project = Project.objects.create(workspace=self.workspace, name='Project A', created_by=self.user)
        ProjectMember.objects.create(project=self.project, user=self.user, role=ProjectMember.Role.OWNER)
        self.status_todo = TaskStatus.objects.create(workspace=self.workspace, name='To Do', order=1, is_default=True)
        self.status_done = TaskStatus.objects.create(workspace=self.workspace, name='Done', order=2)

        self.client.force_authenticate(user=self.user)

    def test_create_task_assigns_workspace_and_reporter(self):
        response = self.client.post(
            '/api/v1/tasks/',
            {
                'project': self.project.id,
                'title': 'Initial task',
                'description': 'Task description',
                'priority': 'high',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(title='Initial task')
        self.assertEqual(task.workspace, self.workspace)
        self.assertEqual(task.reporter, self.user)
        self.assertEqual(task.status, self.status_todo)

    def test_task_list_is_workspace_scoped(self):
        own = Task.objects.create(
            workspace=self.workspace,
            project=self.project,
            title='Own',
            reporter=self.user,
            status=self.status_todo,
        )
        other_project = Project.objects.create(
            workspace=self.other_workspace,
            name='Other Project',
            created_by=self.other_user,
        )
        ProjectMember.objects.create(project=other_project, user=self.other_user, role=ProjectMember.Role.OWNER)
        other_status = TaskStatus.objects.create(workspace=self.other_workspace, name='Other', order=1, is_default=True)
        other = Task.objects.create(
            workspace=self.other_workspace,
            project=other_project,
            title='Other',
            reporter=self.other_user,
            status=other_status,
        )

        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {item['id'] for item in response.data['results']}
        self.assertIn(own.id, ids)
        self.assertNotIn(other.id, ids)

    def test_filter_search_ordering(self):
        t1 = Task.objects.create(
            workspace=self.workspace,
            project=self.project,
            title='Alpha task',
            description='first',
            reporter=self.user,
            status=self.status_todo,
            priority='low',
        )
        t2 = Task.objects.create(
            workspace=self.workspace,
            project=self.project,
            title='Beta task',
            description='second',
            reporter=self.user,
            status=self.status_done,
            priority='high',
        )

        filtered = self.client.get(f'/api/v1/tasks/?status={self.status_done.id}')
        self.assertEqual(filtered.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filtered.data['results']), 1)
        self.assertEqual(filtered.data['results'][0]['id'], t2.id)

        searched = self.client.get('/api/v1/tasks/?search=alpha')
        self.assertEqual(searched.status_code, status.HTTP_200_OK)
        self.assertEqual(len(searched.data['results']), 1)
        self.assertEqual(searched.data['results'][0]['id'], t1.id)

        ordered = self.client.get('/api/v1/tasks/?ordering=priority')
        self.assertEqual(ordered.status_code, status.HTTP_200_OK)
        self.assertEqual(ordered.data['results'][0]['priority'], 'high')
