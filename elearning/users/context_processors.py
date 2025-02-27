from .models import AppUser
from courses.models import Notification

def notifications(request):
  notifications_count = 0
  notifications = []

  if request.user.is_authenticated:
    app_user = AppUser.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=app_user).order_by('-time_created')
    notifications_count = notifications.filter(read=False).count()

  return {'notifications_count': notifications_count, 'notifications': notifications}
