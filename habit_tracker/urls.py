from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version='v1',
        description="API для трекера привычек по книге «Атомные привычки»",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def home(request):
    return HttpResponse("""
        <h1>Habit Tracker API</h1>
        <p>Добро пожаловать в API трекера привычек!</p>
        <h2>Документация:</h2>
        <ul>
            <li><a href='/swagger/'>Swagger UI</a> - интерактивная документация</li>
            <li><a href='/redoc/'>ReDoc</a> - альтернативная документация</li>
            <li><a href='/admin/'>Admin panel</a></li>
        </ul>
        <h2>Доступные эндпоинты:</h2>
        <ul>
            <li><b>GET /api/habits/</b> - список моих привычек</li>
            <li><b>POST /api/habits/</b> - создать привычку</li>
            <li><b>GET /api/habits/{id}/</b> - детали привычки</li>
            <li><b>PUT /api/habits/{id}/</b> - обновить привычку</li>
            <li><b>DELETE /api/habits/{id}/</b> - удалить привычку</li>
            <li><b>GET /api/public-habits/</b> - список публичных привычек</li>
        </ul>
    """)

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('habits.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]