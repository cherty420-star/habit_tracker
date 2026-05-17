from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Habit


@shared_task
def send_habit_reminders():
    """Проверка привычек и отправка напоминаний (в лог)"""
    now = timezone.now()
    current_time = now.time()

    print(f"\n🕐 [{now.strftime('%Y-%m-%d %H:%M:%S')}] Проверка привычек...")

    # Находим привычки, которые нужно выполнить в ближайшие 5 минут
    habits = Habit.objects.filter(is_pleasant=False)
    notified = 0

    for habit in habits:
        habit_time = habit.time
        time_diff = datetime.combine(now.date(), habit_time) - datetime.combine(now.date(), current_time)

        # Если время привычки наступило или скоро наступит
        if 0 <= time_diff.total_seconds() <= 300:
            # Проверяем периодичность
            days_since_created = (now.date() - habit.created_at.date()).days
            if days_since_created % habit.periodicity == 0:
                # Отправляем уведомление
                log_notification.delay(
                    habit.user.id,
                    habit.action,
                    habit.place,
                    habit.time,
                    habit.duration
                )
                notified += 1

    print(f"✅ Обработано привычек: {habits.count()}, отправлено уведомлений: {notified}")
    return f"Notified: {notified}"


@shared_task
def log_notification(user_id, action, place, time, duration):
    """Логирование уведомлений"""
    print(f"""
    📢 [УВЕДОМЛЕНИЕ]
    Пользователь ID: {user_id}
    Действие: {action}
    Место: {place}
    Время: {time}
    Длительность: {duration} сек.
    """)
    return f"Notification logged for user {user_id}"