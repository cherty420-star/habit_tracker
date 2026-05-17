import requests
import time
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')
django.setup()

from users.models import User

TOKEN = '8599977113:AAFS_YWzjtMwO6Mvvcm-UrvpMzgIYGzOVi0'


def send_message(chat_id, text):
    """Отправить сообщение в Telegram"""
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    try:
        response = requests.post(
            url,
            json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'},
            timeout=30
        )
        if response.status_code == 200:
            print(f"✅ Сообщение отправлено в {chat_id}")
            return response.json()
        else:
            print(f"❌ Ошибка: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return None


def get_updates(offset=None):
    """Получить новые сообщения от пользователей"""
    url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    params = {'timeout': 30, 'offset': offset}
    try:
        response = requests.get(url, params=params, timeout=35)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка получения обновлений: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def main():
    print("🤖 Telegram бот запущен...")
    print(f"📱 Имя бота: @Andrew96_habbit_bot")
    print("💬 Напишите /start в Telegram")
    print("-" * 50)

    last_update_id = None

    while True:
        try:
            updates = get_updates(last_update_id)

            if updates and updates.get('ok'):
                for update in updates.get('result', []):
                    last_update_id = update['update_id'] + 1

                    if 'message' in update:
                        chat_id = update['message']['chat']['id']
                        text = update['message'].get('text', '')
                        username = update['message']['from'].get('username', 'Без имени')

                        print(f"📩 Получено сообщение от @{username} (ID: {chat_id}): {text}")

                        if text == '/start':
                            # Сохраняем пользователя
                            user, created = User.objects.get_or_create(
                                username=f'telegram_{chat_id}',
                                defaults={
                                    'telegram_chat_id': chat_id,
                                    'email': f'telegram_{chat_id}@temp.com'
                                }
                            )
                            if not created and user.telegram_chat_id != chat_id:
                                user.telegram_chat_id = chat_id
                                user.save()
                                print(f"💾 Обновлён пользователь: {user.username}")
                            else:
                                print(f"✅ Создан новый пользователь: {user.username}")

                            send_message(chat_id,
                                         f"🤖 <b>Привет, {username}!</b>\n\n"
                                         f"Я бот для напоминания о полезных привычках!\n\n"
                                         f"✅ Твой Telegram ID: <code>{chat_id}</code>\n"
                                         f"✅ Твой аккаунт привязан к системе\n\n"
                                         f"💪 Теперь ты будешь получать напоминания о привычках!\n\n"
                                         f"Команды:\n"
                                         f"/start - Начать работу\n"
                                         f"/help - Помощь"
                                         )

                        elif text == '/help':
                            send_message(chat_id,
                                         f"📋 <b>Помощь</b>\n\n"
                                         f"🤖 Я бот для напоминания о привычках\n\n"
                                         f"Команды:\n"
                                         f"/start - Зарегистрироваться\n"
                                         f"/help - Показать это сообщение\n\n"
                                         f"Напоминания приходят автоматически по расписанию"
                                         )
                        else:
                            send_message(chat_id,
                                         f"❓ Неизвестная команда\n"
                                         f"Используй /start или /help"
                                         )

            time.sleep(2)

        except KeyboardInterrupt:
            print("\n👋 Бот остановлен")
            break
        except Exception as e:
            print(f"❌ Ошибка в основном цикле: {e}")
            time.sleep(5)


if __name__ == '__main__':
    main()