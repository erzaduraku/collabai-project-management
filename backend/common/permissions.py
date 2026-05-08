from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        owner = getattr(obj, 'user', None)
        return owner is not None and owner == user


class IsWorkspaceMember(BasePermission):
    message = 'You must belong to a workspace to access this resource.'

    def _workspace_id_from_object(self, obj):
        workspace_id = getattr(obj, 'workspace_id', None)
        if workspace_id:
            return workspace_id
        project = getattr(obj, 'project', None)
        if project is not None:
            return getattr(project, 'workspace_id', None)
        task = getattr(obj, 'task', None)
        if task is not None:
            return getattr(task, 'workspace_id', None)
        return None

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, 'profile', None)
        return profile is not None and profile.workspace_id is not None

    def has_object_permission(self, request, view, obj):
        profile = getattr(request.user, 'profile', None)
        if profile is None or profile.workspace_id is None:
            return False
        object_workspace_id = self._workspace_id_from_object(obj)
        return object_workspace_id == profile.workspace_id


class IsProjectMember(BasePermission):
    message = 'You must be a project member to access this resource.'

    def _project_from_obj(self, obj):
        if hasattr(obj, 'members'):
            return obj
        project = getattr(obj, 'project', None)
        if project is not None:
            return project
        task = getattr(obj, 'task', None)
        if task is not None:
            return getattr(task, 'project', None)
        return None

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        return bool(user and user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        project = self._project_from_obj(obj)
        if project is None:
            return False
        return project.members.filter(user=request.user).exists() or project.created_by_id == request.user.id
