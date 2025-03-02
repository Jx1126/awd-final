from django.contrib import admin
from .models import Course, CourseFeedback, CourseMaterial, Notification

admin.site.register(Course)
admin.site.register(CourseFeedback)
admin.site.register(CourseMaterial)
admin.site.register(Notification)