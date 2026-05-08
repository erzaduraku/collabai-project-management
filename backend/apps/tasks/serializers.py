from rest_framework import serializers

from apps.projects.models import Project
from .models import Task, TaskStatus


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ['id', 'name', 'order', 'is_default']


class TaskListSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    assignee_email = serializers.EmailField(source='assignee.email', read_only=True)
    reporter_email = serializers.EmailField(source='reporter.email', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'project',
            'title',
            'priority',
            'status',
            'status_name',
            'assignee',
            'assignee_email',
            'reporter',
            'reporter_email',
            'due_date',
            'completed_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'reporter', 'reporter_email', 'created_at', 'updated_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    status = TaskStatusSerializer(read_only=True)
    assignee_email = serializers.EmailField(source='assignee.email', read_only=True)
    reporter_email = serializers.EmailField(source='reporter.email', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'workspace',
            'project',
            'title',
            'description',
            'priority',
            'status',
            'assignee',
            'assignee_email',
            'reporter',
            'reporter_email',
            'due_date',
            'completed_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'workspace', 'reporter', 'reporter_email', 'created_at', 'updated_at']


class TaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'status', 'assignee', 'priority', 'due_date', 'completed_at']
        read_only_fields = ['id']

    def validate_project(self, value):
        request = self.context['request']
        workspace_id = request.user.profile.workspace_id
        if value.workspace_id != workspace_id:
            raise serializers.ValidationError('Project must belong to your workspace.')
        if not (value.members.filter(user=request.user).exists() or value.created_by_id == request.user.id):
            raise serializers.ValidationError('You must be a project member.')
        return value

    def validate_status(self, value):
        request = self.context['request']
        workspace_id = request.user.profile.workspace_id
        if value and value.workspace_id != workspace_id:
            raise serializers.ValidationError('Status must belong to your workspace.')
        return value

    def validate(self, attrs):
        project = attrs.get('project', getattr(self.instance, 'project', None))
        status = attrs.get('status', getattr(self.instance, 'status', None))
        if project and status and project.workspace_id != status.workspace_id:
            raise serializers.ValidationError({'status': 'Status workspace must match project workspace.'})
        return attrs
