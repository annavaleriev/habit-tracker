from rest_framework import serializers
from habits.models import Habit
from habits.validators import validate_reward_or_linked_habit, validate_duration, \
    validate_linked_habit_is_pleasant_habit, validate_pleasant_habit_reward


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычек"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    duration = serializers.DurationField(validators=[validate_duration])
    periodicity = serializers.IntegerField(max_value=7, min_value=1)

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        reward = data.get("reward")
        linked_habit = data.get("linked_habit")
        pleasant_habit = data.get("pleasant_habit")
        # Проверяем, что указана награда или связанная привычка
        validate_reward_or_linked_habit(reward, linked_habit)
        # Проверяем, что связанная привычка приятная
        validate_linked_habit_is_pleasant_habit(linked_habit, pleasant_habit)
        # Проверяем, что у приятной привычки нет награды или связанной привычки
        validate_pleasant_habit_reward(pleasant_habit, reward)

        return data
