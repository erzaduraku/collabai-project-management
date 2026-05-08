from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from common.permissions import IsProjectMember, IsWorkspaceMember

from .models import Comment
from .serializers import CommentDetailSerializer, CommentListSerializer, CommentWriteSerializer


@extend_schema_view(
    list=extend_schema(tags=['Comments'], summary='List comments'),
    retrieve=extend_schema(tags=['Comments'], summary='Retrieve comment'),
    create=extend_schema(tags=['Comments'], summary='Create comment'),
    update=extend_schema(tags=['Comments'], summary='Update comment'),
    partial_update=extend_schema(tags=['Comments'], summary='Partially update comment'),
    destroy=extend_schema(tags=['Comments'], summary='Delete comment'),
)
class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsWorkspaceMember, IsProjectMember]
    filterset_fields = ['task', 'author']
    search_fields = ['body']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        workspace_id = user.profile.workspace_id
        return (
            Comment.objects.filter(workspace_id=workspace_id)
            .filter(Q(task__project__created_by=user) | Q(task__project__members__user=user))
            .select_related('workspace', 'task', 'author', 'task__project')
            .distinct()
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return CommentWriteSerializer
        return CommentDetailSerializer

    def perform_create(self, serializer):
        serializer.save(
            workspace=self.request.user.profile.workspace,
            author=self.request.user,
        )
