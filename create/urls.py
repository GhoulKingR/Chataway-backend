from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_acc),
    path('login', views.login),
    path('chats', views.get_chat),
    path('send', views.send),
]