from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly


class HabitPagination(LimitOffsetPagination):
    """Пагинация по 5 привычек на страницу"""
    default_limit = 5
    max_limit = 100


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Возвращает привычки пользователя или публичные"""
        # Если запрошены публичные привычки
        if self.request.query_params.get('public') == 'true':
            return Habit.objects.filter(is_public=True)
        # Иначе привычки текущего пользователя
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании автоматически назначаем пользователя"""
        serializer.save(user=self.request.user)


class PublicHabitList(generics.ListAPIView):
    """Список публичных привычек"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)