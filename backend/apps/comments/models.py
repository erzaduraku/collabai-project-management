from django.conf import settings
from django.db import models

from apps.tasks.models import Task
from apps.workspaces.models import Workspace
from common.models import BaseModel


class Comment(BaseModel):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    body = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment #{self.pk} on {self.task.title}'
