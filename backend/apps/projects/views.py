from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from common.permissions import IsWorkspaceMember

from .models import Project, ProjectMember
from .serializers import ProjectDetailSerializer, ProjectListSerializer, ProjectWriteSerializer


@extend_schema_view(
    list=extend_schema(tags=['Projects'], summary='List projects'),
    retrieve=extend_schema(tags=['Projects'], summary='Retrieve project'),
    create=extend_schema(tags=['Projects'], summary='Create project'),
    update=extend_schema(tags=['Projects'], summary='Update project'),
    partial_update=extend_schema(tags=['Projects'], summary='Partially update project'),
    destroy=extend_schema(tags=['Projects'], summary='Delete project'),
)
class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsWorkspaceMember]
    filterset_fields = ['status', 'created_by', 'start_date', 'due_date']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'name', 'start_date', 'due_date']
    ordering = ['-created_at']

    def get_queryset(self):
        workspace_id = self.request.user.profile.workspace_id
        return (
            Project.objects.filter(workspace_id=workspace_id)
            .filter(Q(created_by=self.request.user) | Q(members__user=self.request.user))
            .select_related('workspace', 'created_by')
            .prefetch_related('members__user')
            .distinct()
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectWriteSerializer
        return ProjectDetailSerializer

    def perform_create(self, serializer):
        project = serializer.save(
            workspace=self.request.user.profile.workspace,
            created_by=self.request.user,
        )
        ProjectMember.objects.get_or_create(
            project=project,
            user=self.request.user,
            defaults={'role': ProjectMember.Role.OWNER},
        )
