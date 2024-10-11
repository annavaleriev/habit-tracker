import factory
from django.utils import timezone
from factory import fuzzy

from habits.models import Habit
from users.models import User

from datetime import time as dt_time
import random


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания пользователей"""
    email = factory.LazyAttribute(
        lambda n: "{}.{}@example.com".format(n.first_name, n.last_name).lower()
    )
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    # tg_user_id = factory.Faker("random_int", min=1, max=1000000000)

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Создаем пользователя через UserManager для хеширования пароля"""
        # manager = model_class.objects
        # return model_class.default_manager.create_user(*args, **kwargs)
        return User.objects.create_user(*args, **kwargs)


class HabitFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания привычек"""
    user = factory.SubFactory(UserFactory)
    place = factory.Faker("address")
    time = factory.LazyFunction(lambda: dt_time(random.randint(0, 23), random.randint(0, 59)))
    habit_name = factory.Faker("word")
    pleasant_habit = factory.Faker("boolean")
    linked_habit = None
    periodicity = fuzzy.FuzzyInteger(1, 7)
    reward = factory.Faker("sentence")
    duration = factory.Faker("time_delta", end_datetime=timezone.timedelta(minutes=2))
    is_public = factory.Faker("boolean")

    class Meta:
        model = Habit
