from rest_framework import permissions

__all__ = [
    'IsOwnerOrReadOnly',
    'IsAdminOrReadOnly'
]


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    作成者のみがWrite権限をもち、他はReadOnlyなパーミッション
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        import sys
        print(f'{obj.owner.id} {request.user.id} {obj.owner == request.user}', file=sys.stderr)
        return obj.owner == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    管理者のみがWrite権限を持ち、他はReadOnlyなパーミッション
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.is_staff
