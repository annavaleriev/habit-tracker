# Generated by Django 5.1.1 on 2024-10-07 16:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(help_text='Введите место, где вы выполняете привычку', max_length=150, verbose_name='Место')),
                ('time', models.TimeField(help_text='Введите время, когда вы выполняете привычку', verbose_name='Время')),
                ('habit_name', models.CharField(help_text='Введите название привычки', max_length=255, verbose_name='Название привычки')),
                ('pleasant_habit', models.BooleanField(help_text='Укажите является ли привычка приятной', verbose_name='Приятная привычка')),
                ('periodicity', models.CharField(choices=[('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')], default='daily', help_text='Выберите периодичность привычки', max_length=50, verbose_name='Периодичность')),
                ('reward', models.CharField(help_text='Введите награду за выполнение привычки', max_length=150, verbose_name='Вознаграждение')),
                ('duration', models.DurationField(help_text='Введите время выполнения привычки (не более 2х минут', verbose_name='Длительность привычки')),
                ('is_public', models.BooleanField(help_text='Является ли привычка публичной?', verbose_name='Публичная привычка')),
                ('linked_habit', models.ForeignKey(blank=True, help_text='Связанная привычка (для полезных привычек)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habit', verbose_name='Связанная привычка')),
                ('user', models.ForeignKey(help_text='Владелец привычки', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
                'ordering': ['user', 'habit_name'],
            },
        ),
    ]
