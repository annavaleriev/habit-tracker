from rest_framework import serializers
from habits.models import Habit
from habits.validators import validate_reward_or_linked_habit, validate_duration, \
    validate_linked_habit_is_pleasant_habit, validate_pleasant_habit_reward_or_linked_habit, validate_periodicity


# video = serializers.URLField(validators=[validate_youtube_link])
class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычек"""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        validate_reward_or_linked_habit(data.get("reward"), data.get("linked_habit")) # Проверяем, что указана награда или связанная привычка
        validate_duration(data.get("duration")) # Проверяем длительность привычки
        validate_linked_habit_is_pleasant_habit(data.get("linked_habit"), data.get("pleasant_habit")) # Проверяем, что связанная привычка приятная
        validate_pleasant_habit_reward_or_linked_habit(data.get("pleasant_habit"), data.get("reward"), data.get("linked_habit")) # Проверяем, что у приятной привычки нет награды или связанной привычки
        validate_periodicity(data.get("periodicity")) # Проверяем периодичность привычки
        return data

