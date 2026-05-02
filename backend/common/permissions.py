from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        owner = getattr(obj, 'user', None)
        return owner is not None and owner == user
