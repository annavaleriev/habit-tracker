from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwnerOrReadOnly
from habits.serializer import HabitSerializer


class HabitListCreateView(generics.ListCreateAPIView):
    """Представление для списка и создания привычек"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get_queryset(self):
        """Получение списка привычек для текущего пользователя"""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создание привычки"""
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления привычек"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Habit.objects.all()


class HabitPublicListView(generics.ListAPIView):
    """Представление для получения публичных привычек"""
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPaginator

    def get_queryset(self):
        """Получение списка публичных привычек"""
        return Habit.objects.filter(is_public=True)
