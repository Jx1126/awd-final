from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.appuser.is_teacher
  
class IsStudent(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.appuser.is_student