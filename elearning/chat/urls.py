from django.urls import path
from django.contrib.auth.decorators import login_required
from chat import views as chat_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', login_required(login_url='/user/login/')(chat_views.search_room), name='search_room'),
  path('<str:room_name>/', login_required(login_url='/user/login/')(chat_views.chat_room), name='chat_room'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)