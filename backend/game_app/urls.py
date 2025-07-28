from django.urls import path
from . import views

app_name = 'game_app'

urlpatterns = [
    # API endpoints
    path('play/', views.play_game, name='play_game'),
    path('history/', views.game_history, name='game_history'),
    path('statistics/', views.user_statistics, name='user_statistics'),
] 