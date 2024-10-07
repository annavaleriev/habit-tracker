from users.models import User
from django.contrib import admin


@admin.register(User)  # Регистрируем модель User в админке
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "tg_user_id", "is_active")  # Поля для отображения в админке
    exclude = ("password",)
    filter_horizontal = ("groups", "user_permissions")
