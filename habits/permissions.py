from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Права доступа: владелец может редактировать, остальные только читать публичные"""

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено для публичных привычек или для владельца
        if request.method in SAFE_METHODS:
            return obj.is_public or obj.user == request.user
        # Изменение только для владельца
        return obj.user == request.user