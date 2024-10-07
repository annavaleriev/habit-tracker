from rest_framework import viewsets, generics

from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.serializer import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):  # Создаем ViewSet для пользователей
    queryset = User.objects.all()  # Получаем всех пользователей
    serializer_class = UserSerializer  # Используем сериализатор
    permission_classes = [
        IsAuthenticated
    ]  # Устанавливаем права доступа только для авторизованных пользователей


class UserCreateView(generics.CreateAPIView):  # Создаем View для создания пользователя
    queryset = User.objects.all()  # Получаем всех пользователей
    serializer_class = UserSerializer  # Используем сериализатор
    # permission_classes = [AllowAny] # Устанавливаем права доступа для всех пользователей
    permission_classes = (
        AllowAny,
    )  # Устанавливаем права доступа для всех пользователей

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)  # Создаем пользователя
        user.set_password(user.password)  # Хешируем пароль
        user.save()
