from django.db import models
from common.models import BaseModel
from apps.organizations.models import Organization


class Permission(BaseModel):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class Workspace(BaseModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="workspaces"
    )
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("organization", "name")

    def __str__(self):
        return f"{self.organization.name} - {self.name}"


class Role(BaseModel):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="roles"
    )
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(
        Permission,
        related_name="roles",
        blank=True
    )

    class Meta:
        unique_together = ("workspace", "name")

    def __str__(self):
        return f"{self.workspace.name} - {self.name}"