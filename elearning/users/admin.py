from django.contrib import admin
from .models import AppUser, UserStatusUpdate

admin.site.register(AppUser)
admin.site.register(UserStatusUpdate)