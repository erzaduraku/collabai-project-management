from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.organizations.models import Organization
from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task, TaskStatus
from apps.user_profiles.models import Profile
from apps.workspaces.models import Workspace
from .models import Comment


User = get_user_model()


class CommentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        org = Organization.objects.create(name='Comments Org')
        self.workspace = Workspace.objects.create(name='Comments WS', organization=org)

        self.user = User.objects.create_user(username='author', email='author@example.com', password='StrongPass123!')
        Profile.objects.create(user=self.user, workspace=self.workspace)
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(workspace=self.workspace, name='Project C', created_by=self.user)
        ProjectMember.objects.create(project=self.project, user=self.user, role=ProjectMember.Role.OWNER)
        self.status = TaskStatus.objects.create(workspace=self.workspace, name='To Do', order=1, is_default=True)
        self.task = Task.objects.create(
            workspace=self.workspace,
            project=self.project,
            title='Task C',
            reporter=self.user,
            status=self.status,
        )

    def test_create_comment(self):
        response = self.client.post(
            '/api/v1/comments/',
            {'task': self.task.id, 'body': 'First comment'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get(task=self.task)
        self.assertEqual(comment.workspace, self.workspace)
        self.assertEqual(comment.author, self.user)

    def test_comment_list_filter_and_search(self):
        c1 = Comment.objects.create(workspace=self.workspace, task=self.task, author=self.user, body='Alpha')
        c2 = Comment.objects.create(workspace=self.workspace, task=self.task, author=self.user, body='Beta')

        filtered = self.client.get(f'/api/v1/comments/?task={self.task.id}')
        self.assertEqual(filtered.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filtered.data['results']), 2)

        searched = self.client.get('/api/v1/comments/?search=alpha')
        self.assertEqual(searched.status_code, status.HTTP_200_OK)
        self.assertEqual(len(searched.data['results']), 1)
        self.assertEqual(searched.data['results'][0]['id'], c1.id)
        self.assertNotEqual(c1.id, c2.id)
