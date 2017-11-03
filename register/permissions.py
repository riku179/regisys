from rest_framework import permissions

__all__ = [
    'IsOwnerOrReadOnly',
    'IsAdminOrReadOnly',
    'ItemPermission'
]


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    作成者のみがWrite権限をもち、他はReadOnlyなパーミッション
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner.id == request.user.id


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    管理者のみがWrite権限を持ち、他はReadOnlyなパーミッション
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff


class ItemPermission(IsOwnerOrReadOnly):
    """
    ownerのidは自分のidであることを保証
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.data.get('owner') and int(request.data.get('owner')) != request.user.id:
            return False

        return True
