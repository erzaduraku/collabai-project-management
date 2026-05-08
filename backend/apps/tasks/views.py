from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from common.permissions import IsProjectMember, IsWorkspaceMember

from .models import Task, TaskStatus
from .serializers import TaskDetailSerializer, TaskListSerializer, TaskWriteSerializer


@extend_schema_view(
    list=extend_schema(tags=['Tasks'], summary='List tasks'),
    retrieve=extend_schema(tags=['Tasks'], summary='Retrieve task'),
    create=extend_schema(tags=['Tasks'], summary='Create task'),
    update=extend_schema(tags=['Tasks'], summary='Update task'),
    partial_update=extend_schema(tags=['Tasks'], summary='Partially update task'),
    destroy=extend_schema(tags=['Tasks'], summary='Delete task'),
)
class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsWorkspaceMember, IsProjectMember]
    filterset_fields = ['project', 'status', 'assignee', 'priority', 'due_date', 'completed_at']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        workspace_id = user.profile.workspace_id
        return (
            Task.objects.filter(workspace_id=workspace_id)
            .filter(Q(project__created_by=user) | Q(project__members__user=user))
            .select_related('workspace', 'project', 'status', 'assignee', 'reporter')
            .distinct()
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return TaskWriteSerializer
        return TaskDetailSerializer

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        status = serializer.validated_data.get('status')
        if status is None:
            status = (
                TaskStatus.objects.filter(workspace=project.workspace, is_default=True)
                .order_by('order', 'id')
                .first()
            )
        serializer.save(
            workspace=self.request.user.profile.workspace,
            reporter=self.request.user,
            status=status,
        )
