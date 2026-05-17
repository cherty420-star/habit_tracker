from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'time', 'place', 'is_public', 'is_pleasant')
    list_filter = ('is_public', 'is_pleasant', 'periodicity')
    search_fields = ('action', 'place', 'user__username')
    readonly_fields = ('created_at',)