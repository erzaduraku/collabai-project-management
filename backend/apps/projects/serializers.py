from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project, ProjectMember


User = get_user_model()


class ProjectMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'user_email', 'role', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_email']


class ProjectListSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(source='members.count', read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'status',
            'start_date',
            'due_date',
            'member_count',
            'created_by',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_by_email', 'created_at', 'updated_at']


class ProjectDetailSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    members = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'workspace',
            'name',
            'description',
            'status',
            'start_date',
            'due_date',
            'created_by',
            'created_by_email',
            'members',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'workspace', 'created_by', 'created_by_email', 'members', 'created_at', 'updated_at']


class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'start_date', 'due_date']
        read_only_fields = ['id']

    def validate(self, attrs):
        start_date = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        due_date = attrs.get('due_date', getattr(self.instance, 'due_date', None))
        if start_date and due_date and due_date < start_date:
            raise serializers.ValidationError({'due_date': 'Due date must be after or equal to the start date.'})
        return attrs
