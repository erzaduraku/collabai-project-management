from rest_framework import serializers

from .models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'task',
            'author',
            'author_email',
            'body',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'author_email', 'created_at', 'updated_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'workspace',
            'task',
            'author',
            'author_email',
            'body',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'workspace', 'author', 'author_email', 'created_at', 'updated_at']


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'task', 'body']
        read_only_fields = ['id']

    def validate_task(self, value):
        request = self.context['request']
        workspace_id = request.user.profile.workspace_id
        if value.workspace_id != workspace_id:
            raise serializers.ValidationError('Task must belong to your workspace.')
        project = value.project
        if not (project.members.filter(user=request.user).exists() or project.created_by_id == request.user.id):
            raise serializers.ValidationError('You must be a project member to comment.')
        return value
