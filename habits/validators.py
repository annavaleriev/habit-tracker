from django.core.exceptions import ValidationError


def validate_reward_or_linked_habit(reward, linked_habit):
    """Валидатор для проверки награды и связанной привычки"""
    if reward and linked_habit:
        raise ValidationError(
            "Нельзя указать награду и связанную привычку одновременно"
        )


def validate_duration(duration):
    """Валидатор для проверки длительности привычки"""
    if duration.total_seconds() > 120:
        raise ValidationError(
            "Длительность привычки не должна превышать 2 минут"
        )


def validate_linked_habit_is_pleasant_habit(linked_habit, pleasant_habit):
    """Валидатор для проверки связанной привычки, что она приятная"""
    if linked_habit and not pleasant_habit:
        raise ValidationError(
            "Связанная привычка должна быть приятной"
        )


def validate_pleasant_habit_reward_or_linked_habit(pleasant_habit, reward, linked_habit):
    """Валидатор для проверки, что у приятной привычки не может быть
    вознаграждения или связанной привычки"""
    if pleasant_habit:
        if reward or linked_habit:
            raise ValidationError(
                "Приятная привычка не может иметь награды или связанной привычки"
            )


def validate_periodicity(periodicity):
    """Валидатор для проверки периодичности привычки"""
    if periodicity > 7:
        raise ValidationError(
            "Привычка должна выполняться раз в 7 дней"
        )
