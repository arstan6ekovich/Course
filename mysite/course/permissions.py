from rest_framework.permissions import BasePermission

class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'


class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class StudentOrTeacherOrAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['admin', 'teacher']:
            return True
        elif request.user.role == 'student':
            return obj.student.user == request.user
        return False