from rest_framework import serializers
from .models import Habit


class HabitValidator:
    """Валидатор для привычек"""

    def __call__(self, data):
        # 1. Исключить одновременный выбор связанной привычки и вознаграждения
        if data.get('related_habit') and data.get('reward'):
            raise serializers.ValidationError(
                'Нельзя указать одновременно связанную привычку и вознаграждение'
            )

        # 2. В связанные привычки могут попадать только привычки с признаком приятной привычки
        if data.get('related_habit') and not data['related_habit'].is_pleasant:
            raise serializers.ValidationError(
                'Связанная привычка должна быть приятной'
            )

        # 3. У приятной привычки не может быть вознаграждения или связанной привычки
        if data.get('is_pleasant'):
            if data.get('reward'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть вознаграждения'
                )
            if data.get('related_habit'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть связанной привычки'
                )

        # 4. Время выполнения не больше 120 секунд (проверяется в модели)

        return data


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
        validators = [HabitValidator()]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)