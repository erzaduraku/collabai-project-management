from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from common.permissions import IsProjectMember, IsWorkspaceMember

from .models import ActivityLog
from .serializers import ActivityLogDetailSerializer, ActivityLogListSerializer


@extend_schema_view(
    list=extend_schema(tags=['Activity Logs'], summary='List activity logs'),
    retrieve=extend_schema(tags=['Activity Logs'], summary='Retrieve activity log'),
)
class ActivityLogViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsWorkspaceMember, IsProjectMember]
    filterset_fields = ['project', 'task', 'comment', 'user', 'action']
    search_fields = ['action']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        workspace_id = user.profile.workspace_id
        return (
            ActivityLog.objects.filter(workspace_id=workspace_id)
            .filter(Q(project__created_by=user) | Q(project__members__user=user))
            .select_related('workspace', 'project', 'task', 'comment', 'user')
            .distinct()
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ActivityLogListSerializer
        return ActivityLogDetailSerializer
