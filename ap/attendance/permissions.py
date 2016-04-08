from rest_framework import permissions

## Question - add an owner field for every module so that I can write a global IsOwner permission? 


class AttendanceAllorIsOwner(permissions.BasePermission):
    """
    Custom permission to only allow those with 'attendance_all' or the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
    	if request.user.has_perm('attendance.attendance_all'):
    		return True
        return obj.account == request.user

class AttendanceAll(permissions.BasePermission):
    """
    Custom permission to only allow those with 'attendance_all'.
    """

    def has_permission(self, request, view):
    	if request.user.has_perm('attendance.attendance_all'):
    		return True
    	return False

# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType

# content_type = ContentType.objects.get_for_model(self)
# permission = Permission.objects.create(codename='attendance_all',
#                                        name='Can View All Attendance Records',
                                       # content_type=content_type)

# from django.contrib.auth.models import User, Group, Permission
# from django.contrib.contenttypes.models import ContentType

# content_type = ContentType.objects.get(model='roll')
# permission = Permission.objects.create(codename='can_view',
#                                        name='Can View All Rolls',
#                                        content_type=content_type)

