from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import time
from .models import Habit

User = get_user_model()


class HabitTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        data = {
            'place': 'Home',
            'time': '08:00:00',
            'action': 'Exercise',
            'duration': 60,
            'periodicity': 1
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habit_duration_validation(self):
        data = {
            'place': 'Home',
            'time': '08:00:00',
            'action': 'Exercise',
            'duration': 121,  # Больше 120 секунд
            'periodicity': 1
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)