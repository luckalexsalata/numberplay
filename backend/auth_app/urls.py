from django.urls import path
from . import views

app_name = 'auth_app'

urlpatterns = [
    # API endpoints
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/user/', views.get_user_info, name='get_user_info'),
] 