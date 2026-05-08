from rest_framework import serializers

from .models import ActivityLog


class ActivityLogListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            'id',
            'workspace',
            'project',
            'task',
            'comment',
            'user',
            'user_email',
            'action',
            'metadata',
            'created_at',
        ]
        read_only_fields = fields


class ActivityLogDetailSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            'id',
            'workspace',
            'project',
            'task',
            'comment',
            'user',
            'user_email',
            'action',
            'metadata',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields
