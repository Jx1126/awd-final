from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', user_views.user_register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', login_required(login_url='/user/login/')(user_views.user_logout), name='logout'),
    path('home/', login_required(login_url='/user/login/')(user_views.homepage), name='home'),
    path('search/', login_required(login_url='/user/login/')(user_views.search_users), name='search_users'),
    path('search/<int:user_id>/', login_required(login_url='/user/login/')(user_views.show_profile), name='show_profile'),
    path('search/<int:user_id>/info/', login_required(login_url='/user/login/')(user_views.show_information), name='show_information'),
    path('notification/', login_required(login_url='/user/login/')(user_views.all_notifications), name='all_notifications'),
    path('profile/', login_required(login_url='/user/login/')(user_views.user_profile), name='user_profile'),
    path('profile/edit/', login_required(login_url='/user/login/')(user_views.edit_profile), name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)