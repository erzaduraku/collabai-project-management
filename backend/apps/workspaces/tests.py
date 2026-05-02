from django.test import TestCase
from apps.organizations.models import Organization
from .models import Workspace, Role, Permission


class WorkspaceModelTest(TestCase):
    def test_workspace_creation(self):
        org = Organization.objects.create(name="Org")
        workspace = Workspace.objects.create(name="WS", organization=org)

        self.assertEqual(workspace.organization, org)


class RolePermissionTest(TestCase):
    def test_role_permission(self):
        org = Organization.objects.create(name="Org")
        ws = Workspace.objects.create(name="WS", organization=org)

        perm = Permission.objects.create(code="create_task", name="Create Task")
        role = Role.objects.create(name="Admin", workspace=ws)
        role.permissions.add(perm)

        self.assertIn(perm, role.permissions.all())