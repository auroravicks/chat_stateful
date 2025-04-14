from . import views
from django.urls import path

urlpatterns = [
    path('', views.register, name='register'),
    path('chat/', views.chatbot, name='chatbot'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout')
]