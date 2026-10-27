def user_roles(request):
    """
    Context processor that provides user authorization roles to all templates.
    """
    if not request.user.is_authenticated:
        return {
            'is_instructor': False,
            'is_student': False,
            'user_role': 'Guest',
        }

    is_admin = request.user.is_superuser
    is_instructor = is_admin or request.user.groups.filter(name='Instructor').exists()
    is_student = request.user.groups.filter(name='Student').exists()

    if is_admin:
        role = 'Admin'
    elif is_instructor:
        role = 'Instructor'
    elif is_student:
        role = 'Student'
    else:
        role = 'User'

    return {
        'is_instructor': is_instructor,
        'is_student': is_student,
        'user_role': role,
    }
