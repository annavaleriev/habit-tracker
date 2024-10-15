#!/bin/sh

# Прекращаем выполнение при ошибках
set -e

# Проверка миграций и их применение
echo "Применение миграций базы данных"
python manage.py migrate --noinput

# Создание суперпользователя, если он не существует
echo "Создание суперпользователя, если его нет"
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"root@root.root"}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-"root"}

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Суперпользователь создан')
else:
    print('Суперпользователь уже существует')
END

# Запуск сервера
exec "$@"
