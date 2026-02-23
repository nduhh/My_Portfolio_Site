from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('projects/', views.projects, name='projects'),
    path('about/', views.about, name='about'),
]