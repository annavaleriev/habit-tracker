from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.tests.fabrics import UserFactory, HabitFactory


class HabitTestCase(APITestCase):
    """Тесты для привычек"""

    def setUp(self):  # Создаем клиент
        self.client = APIClient()  # Создаем клиент
        self.habit_list_url = reverse("habits:habit-list")  # Получаем url для списка привычек

    def authenticate_user(self, user):
        """Аутентификация пользователя"""
        self.client.force_authenticate(user=user)

    def create_habit(self, user, **kwargs):
        """Создаем привычку"""
        self.authenticate_user(user)
        response = self.client.post(self.habit_list_url, data=kwargs)
        return response


class ListHabitTestCase(HabitTestCase):
    """Тесты для списка привычек"""

    def test__get_habits__authenticated_user(self):
        """Получаем привычки для аутентифицированного пользователя"""
        user = UserFactory()
        self.authenticate_user(user)

        habits = HabitFactory.create_batch(5, user=user)
        response = self.client.get(self.habit_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(habits), response.data["count"])

        habits_pk = {habit.pk for habit in habits}
        expected_habits_pk = {habit["id"] for habit in response.data["results"]}
        self.assertEqual(habits_pk, expected_habits_pk)

    def test__get_habits__different_user(self):
        """Тест на недоступность привычек другого пользователя"""
        user_1 = UserFactory()
        user_2 = UserFactory()
        self.authenticate_user(user_1)

        HabitFactory.create_batch(3, user=user_2)
        response = self.client.get(self.habit_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


class CreateHabitTestCase(HabitTestCase):
    """Тесты для создания привычек"""

    def test__post_habit__authenticated_user(self):
        """Создаем привычку для аутентифицированного пользователя"""
        user = UserFactory()
        response = self.create_habit(user, habit_name="Бегать по утрам", place="Парк", time="08:00:00")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test__post_habit__without_required_fields(self):
        """Создаем привычку без обязательных полей"""
        user = UserFactory()
        response = self.create_habit(user, place="Дом", time="07:00:00")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateHabitTestCase(HabitTestCase):
    """Тесты для обновления привычек"""

    def update_habit(self, user, habit, **kwargs):
        """Обновляем привычку"""
        self.client.force_authenticate(user=user)
        response = self.client.patch(reverse("habits:habit-detail", args=[habit.pk]), data=kwargs)
        return response

    def test__patch_habit__authenticated_user(self):
        """Обновляем привычку для аутентифицированного пользователя"""
        user = UserFactory()
        habit = HabitFactory(user=user)
        response = self.update_habit(user, habit, habit_name="Бегать по вечерам")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["habit_name"], "Бегать по вечерам")

    def test__patch_habit__not_owner(self):
        user = UserFactory()
        different_user = UserFactory()
        habit = HabitFactory(user=different_user)
        response = self.update_habit(user, habit, habit_name="Бегать по вечерам")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteHabitTestCase(HabitTestCase):
    """Тесты для удаления привычек"""

    def test__delete_habit__owner_user(self):
        """Удаляем привычку для владельца"""
        user = UserFactory()
        habit = HabitFactory(user=user)
        response = self.client.delete(reverse("habits:habit-detail", args=[habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test__delete_habit__not_owner(self):
        """Удаляем привычку не владельцем"""
        user = UserFactory()
        different_user = UserFactory()
        habit = HabitFactory(user=different_user)
        self.authenticate_user(user)
        response = self.client.delete(reverse("habits:habit-detail", args=[habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
