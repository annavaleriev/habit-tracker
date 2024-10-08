from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminder():
    """Отправка напоминания о привычке"""
    now = timezone.now().time()
    habits = Habit.objects.filter(time=now)
    for habit in habits:

        message = f"Не забудьте сегодня выполнить привычку {habit.habit_name} в {habit.time}"
        send_telegram_message(habit.user.tg_user_id, message)
