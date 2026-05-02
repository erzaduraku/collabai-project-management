from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization
from apps.workspaces.models import Workspace
from .models import Profile

User = get_user_model()


class ProfileModelTest(TestCase):
    def test_profile_creation(self):
        user = User.objects.create(username="testuser")
        org = Organization.objects.create(name="Org")
        ws = Workspace.objects.create(name="WS", organization=org)

        profile = Profile.objects.create(user=user, workspace=ws)

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.workspace, ws)