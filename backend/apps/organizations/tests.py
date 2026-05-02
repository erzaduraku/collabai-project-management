from django.test import TestCase
from .models import Organization


class OrganizationModelTest(TestCase):
    def test_create_organization(self):
        org = Organization.objects.create(name="Test Org")
        self.assertEqual(org.name, "Test Org")
