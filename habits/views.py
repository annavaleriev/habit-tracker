from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwnerOrReadOnly
from habits.serializer import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Q(user=self.request.user) | Q(is_public=True))
