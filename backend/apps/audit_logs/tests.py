from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.comments.models import Comment
from apps.organizations.models import Organization
from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task, TaskStatus
from apps.user_profiles.models import Profile
from apps.workspaces.models import Workspace
from .models import ActivityLog


User = get_user_model()


class ActivityLogApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        organization = Organization.objects.create(name='Audit Org')
        self.workspace = Workspace.objects.create(name='Audit WS', organization=organization)
        self.user = User.objects.create_user(username='logger', email='logger@example.com', password='StrongPass123!')
        Profile.objects.create(user=self.user, workspace=self.workspace)
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(workspace=self.workspace, name='Audit Project', created_by=self.user)
        ProjectMember.objects.create(project=self.project, user=self.user, role=ProjectMember.Role.OWNER)
        status_obj = TaskStatus.objects.create(workspace=self.workspace, name='Open', order=1, is_default=True)
        self.task = Task.objects.create(
            workspace=self.workspace,
            project=self.project,
            title='Audit Task',
            reporter=self.user,
            status=status_obj,
        )
        self.comment = Comment.objects.create(
            workspace=self.workspace,
            task=self.task,
            author=self.user,
            body='Audit comment',
        )
        self.log = ActivityLog.objects.create(
            workspace=self.workspace,
            project=self.project,
            task=self.task,
            comment=self.comment,
            user=self.user,
            action='comment.created',
            metadata={'source': 'api'},
        )

    def test_activity_log_is_read_only(self):
        list_response = self.client.get('/api/v1/audit/activity/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data['results'][0]['id'], self.log.id)

        detail_response = self.client.get(f'/api/v1/audit/activity/{self.log.id}/')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['action'], 'comment.created')

        create_response = self.client.post(
            '/api/v1/audit/activity/',
            {'action': 'x'},
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
