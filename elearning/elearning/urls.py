from django.contrib import admin
from django.urls import path, include
from .views import homepage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('user/', include('users.urls')),
    path('user/course/', include('courses.urls')),
]