from __future__ import annotations

import logging

from celery import shared_task
from django.apps import apps

from .services.indexing import index_instance

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def index_model_instance(self, app_label: str, model_name: str, pk: int) -> str | None:
    model = apps.get_model(app_label, model_name)
    try:
        instance = model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None

    doc_key = index_instance(instance)
    logger.info("Indexed %s:%s -> %s", model_name, pk, doc_key)
    return doc_key


@shared_task
def delete_indexed_document(doc_key: str) -> None:
    from .services.vector_store import get_vector_store

    get_vector_store().delete(doc_key)


@shared_task
def reindex_organization(organization_id: int) -> int:
    from apps.comments.models import ActivityLog, Comment
    from apps.projects.models import Project
    from apps.tasks.models import Task

    count = 0
    for project in Project.objects.filter(organization_id=organization_id):
        index_instance(project)
        count += 1

    tasks = Task.objects.filter(project__organization_id=organization_id)
    for task in tasks:
        index_instance(task)
        count += 1

    for comment in Comment.objects.filter(task__project__organization_id=organization_id):
        index_instance(comment)
        count += 1

    for activity in ActivityLog.objects.filter(task__project__organization_id=organization_id):
        index_instance(activity)
        count += 1

    logger.info("Reindexed organization %s (%s documents)", organization_id, count)
    return count


reindex_workspace = reindex_organization
