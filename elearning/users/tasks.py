from celery import shared_task
from PIL import Image
import time

# Resize the profile photo to reduce the size
@shared_task
def process_profile_photos(user_id):
  from .models import AppUser
  try:
    app_user = AppUser.objects.get(id=user_id)
    if app_user.profile_photo:
      path = app_user.profile_photo.path
      time.sleep(2)
      img = Image.open(path)

      width, height = img.size
      min_dim = min(width, height)

      if min_dim > 300:
        scale_factor = 300 / min_dim
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = img.resize((new_width, new_height), Image.LANCZOS)

      width, height = img.size
      min_dim = min(width, height)

      left = (width - min_dim) / 2
      top = (height - min_dim) / 2
      right = (width + min_dim) / 2
      bottom = (height + min_dim) / 2
      img = img.crop((left, top, right, bottom))

      img.save(path, quality=80, optimize=True)

  except Exception as e:
    return str(e)