from datetime import datetime, timedelta

from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from habits.tasks import send_habit_reminder

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    """Модель для привычек"""

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

    periodicity = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(7)],
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

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        super().save(
            *args,
            force_insert,
            force_update,
            using,
            update_fields,
        )
        now = timezone.now()

        # Получаем время выполнения задачи из модели
        task_time = self.time

        # Планируем задачу на каждый день в течение repeat_days
        for day in range(self.periodicity):
            # Вычисляем дату и время для каждой итерации
            run_at = datetime.combine(
                now.date() + timedelta(days=day),  # День выполнения задачи
                task_time  # Время выполнения задачи
            )

            # Планируем задачу на рассчитанное время
            send_habit_reminder.apply_async(
                args=[self.habit_name, self.time, self.user.tg_user_id],
                eta=run_at  # Указываем точное время выполнения задачи
            )

    def __str__(self):
        return f"Привычка {self.habit_name}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["user", "habit_name"]
