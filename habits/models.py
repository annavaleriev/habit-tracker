from django.db import models

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    """Модель для привычек"""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    PERIODICITY_CHOICES = [
        (DAILY, "Ежедневно"),
        (WEEKLY, "Еженедельно"),
        (MONTHLY, "Ежемесячно"),
    ]

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Владелец привычки",
    )

    place = models.CharField(
        max_length=150,
        verbose_name="Место",
        help_text="Введите место, где вы выполняете привычку",
    )

    time = models.TimeField(
        verbose_name="Время",
        help_text="Введите время, когда вы выполняете привычку",
    )

    habit_name = models.CharField(
        max_length=255,
        verbose_name="Название привычки",
        help_text="Введите название привычки",
    )

    pleasant_habit = models.BooleanField(
        verbose_name="Приятная привычка",
        help_text="Укажите является ли привычка приятной",
    )

    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Связанная привычка",
        help_text="Связанная привычка (для полезных привычек)",
    )

    periodicity = models.CharField(
        max_length=50,
        choices=PERIODICITY_CHOICES,
        default=DAILY,
        verbose_name="Периодичность",
        help_text="Выберите периодичность привычки",
    )

    reward = models.CharField(
        max_length=150,
        verbose_name="Вознаграждение",
        help_text="Введите награду за выполнение привычки",
    )

    duration = models.DurationField(
        verbose_name="Длительность привычки",
        help_text="Введите время выполнения привычки (не более 2х минут",
    )

    is_public = models.BooleanField(
        verbose_name="Публичная привычка",
        help_text="Является ли привычка публичной?",
    )

    def __str__(self):
        return f"Привычка {self.habit_name}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["user", "habit_name"]
