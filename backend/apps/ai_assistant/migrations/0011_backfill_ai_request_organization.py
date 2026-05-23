from django.db import migrations


def backfill_ai_request_organization(apps, schema_editor):
    AIRequest = apps.get_model('ai_assistant', 'AIRequest')
    Task = apps.get_model('tasks', 'Task')

    requests = AIRequest.objects.filter(
        organization__isnull=True,
        task_id__isnull=False,
    )
    for ai_request in requests.iterator():
        organization_id = (
            Task.objects.filter(pk=ai_request.task_id)
            .values_list('project__organization_id', flat=True)
            .first()
        )
        if not organization_id:
            continue
        ai_request.organization_id = organization_id
        ai_request.save(update_fields=['organization'])


class Migration(migrations.Migration):

    dependencies = [
        ('ai_assistant', '0010_airequest_organization_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_ai_request_organization, migrations.RunPython.noop),
    ]
