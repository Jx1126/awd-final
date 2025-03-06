from .models import AppUser
from courses.models import Notification


# Make variables available globally
def global_data(request):
    notifications_count = 0
    notifications = []
    user_profile = None

    if request.user.is_authenticated:
        try:
            app_user = AppUser.objects.get(user=request.user)
            notifications = Notification.objects.filter(user=app_user).order_by(
                "-time_created"
            )
            notifications_count = notifications.filter(read=False).count()
            user_profile = app_user
        except AppUser.DoesNotExist:
            pass

    return {
        "notifications_count": notifications_count,
        "notifications": notifications,
        "user_profile": user_profile,
    }
