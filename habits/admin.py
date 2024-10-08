from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)  # Регистрируем модель Habit в админке
class HabitAdmin(admin.ModelAdmin):
    list_display = ("habit_name", "user", "duration", "periodicity")
    # filter_horizontal = ()
