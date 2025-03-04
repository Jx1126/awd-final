from rest_framework.permissions import BasePermission

def is_teacher(user):
  return hasattr(user, 'appuser') and user.appuser.is_teacher

def is_student(user):
  return hasattr(user, 'appuser') and user.appuser.is_student

class IsTeacher(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.appuser.is_teacher
  
class IsStudent(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.appuser.is_student