from celery import shared_task

from habits.services import send_telegram_message


@shared_task
def send_habit_reminder(habit_name, habit_time, tg_user_id):
    """Отправка напоминания о привычке"""
    message = f"Не забудьте сегодня выполнить привычку {habit_name} в {habit_time}"
    send_telegram_message(tg_user_id, message)
