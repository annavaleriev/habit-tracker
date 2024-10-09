from django.core.exceptions import ValidationError


def validate_reward_or_linked_habit(reward, linked_habit):
    """Валидатор для проверки награды и связанной привычки"""
    if reward and linked_habit:
        raise ValidationError(
            {
                "reward": "Нельзя указать награду и связанную привычку одновременно",
                "linked_habit": "Нельзя указать награду и связанную привычку одновременно",
            }
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
            {
                "linked_habit": "Связанная привычка должна быть приятной",
                "pleasant_habit": "Связанная привычка должна быть приятной",
            }
        )


def validate_pleasant_habit_reward(pleasant_habit, reward):
    """Валидатор для проверки, что у приятной привычки не может быть
    вознаграждения"""
    if pleasant_habit and reward:
        raise ValidationError(
            {
                "pleasant_habit": "Приятная привычка не может иметь награды",
                "reward": "Приятная привычка не может иметь награды",
            }
        )
