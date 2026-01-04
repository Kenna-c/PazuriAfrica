from django.http import HttpResponseForbidden

def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        # Allow superusers
        if user.is_superuser:
            return view_func(request, *args, **kwargs)

        # Ensure profile exists
        if not hasattr(user, 'profile'):
            return HttpResponseForbidden("No profile found")

        # Check role
        if user.profile.role != 'staff':
            return HttpResponseForbidden("Staff access only")

        return view_func(request, *args, **kwargs)
    return wrapper
def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        # Allow superusers
        if user.is_superuser:
            return view_func(request, *args, **kwargs)

        # Ensure profile exists
        if not hasattr(user, 'profile'):
            return HttpResponseForbidden("No profile found")

        # Check role
        if user.profile.role != 'student':
            return HttpResponseForbidden("Student access only")
        return view_func(request, *args, **kwargs)
    return wrapper