from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login')
]
