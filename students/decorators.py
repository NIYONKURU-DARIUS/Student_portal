from functools import wraps
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def allowed_groups(allowed_roles=None):
    """
    Decorator to restrict view access to specific user groups.
    Superusers automatically bypass the check.
    If unauthorized, an informative 403 Access Denied template is rendered.
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_groups = list(request.user.groups.values_list('name', flat=True))
            if any(role in user_groups for role in allowed_roles):
                return view_func(request, *args, **kwargs)

            context = {
                'required_roles': allowed_roles,
                'user_roles': user_groups or ['Student / Viewer'],
                'attempted_action': request.path,
            }
            return render(request, 'students/access_denied.html', context, status=403)
        return wrapper
    return decorator


def instructor_required(view_func):
    """
    Convenience decorator for actions restricted to Instructors and Admins
    (Creating, Editing, Deleting students).
    """
    return allowed_groups(allowed_roles=['Instructor'])(view_func)
