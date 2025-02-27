from django.urls import path
from django.contrib.auth.decorators import login_required
from chat import views as chat_views

urlpatterns = [
  path('', login_required(login_url='/user/login/')(chat_views.index), name='index'),
  path('chat/<str:room_name>/', login_required(login_url='/user/login/')(chat_views.chat_room), name='chat_room'),
]