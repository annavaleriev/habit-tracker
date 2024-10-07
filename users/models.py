from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from django.db import models

NULLABLE = {"blank": True, "null": True}


class UserManager(BaseUserManager):
    """Класс для создания пользователей"""

    use_in_migrations = True  # Переменная для использования в миграциях

    def _create_user(
            self, email, password, **extra_fields
    ):  # Метод для создания пользователя
        if not email:  # Если email не указан
            raise ValueError(
                "У пользователя должен быть адрес электронной почты"
            )  # Выводим ошибку
        email = self.normalize_email(email)  # Нормализуем email
        user = self.model(email=email, **extra_fields)  # Создаем пользователя
        user.set_password(password)  # Хешируем пароль
        user.save(using=self._db)  # Сохраняем пользователя
        return user  # Возвращаем пользователя

    def create_user(
            self, email, password=None, **extra_fields
    ):  # Метод для создания пользователя
        extra_fields.setdefault(
            "is_staff", False
        )  # Устанавливаем значение по умолчанию
        extra_fields.setdefault(
            "is_superuser", False
        )  # Устанавливаем значение по умолчанию
        return self._create_user(
            email, password, **extra_fields
        )  # Создаем пользователя

    def create_superuser(
            self, email, password=None, **extra_fields
    ):  # Метод для создания суперпользователя
        extra_fields.setdefault("is_staff", True)  # Устанавливаем значение по умолчанию
        extra_fields.setdefault(
            "is_superuser", True
        )  # Устанавливаем значение по умолчанию

        if (
                extra_fields.get("is_staff") is not True
        ):  # Если пользователь не является сотрудником
            raise ValueError(
                "Суперпользователь должен иметь is_staff=True"
            )  # Выводим ошибку
        if (
                extra_fields.get("is_superuser") is not True
        ):  # Если пользователь не является суперпользователем
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True."
            )  # Выводим ошибку

        return self._create_user(
            email, password, **extra_fields
        )  # Создаем пользователя


class User(AbstractUser):
    """Класс для создания пользователей"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Введите адрес электронной почты"
    )
    tg_user_id = models.CharField(max_length=255,
                                  **NULLABLE, verbose_name="ID пользователя в телеграмме", unique=True
                                  )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # Объект для работы с пользователями

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return f"Пользователь {self.email} {self.tg_user_id or ''}"
