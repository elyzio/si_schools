from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def group_required(*group_names):
    """
    Decorator that checks if the user belongs to any of the specified groups.
    If not, redirects to the previous page or home with a permission denied message.

    Usage:
        @group_required('admin')
        @group_required('admin', 'staff')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Ita presiza login uluk!')
                return redirect('login')

            # Superusers have access to everything
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check if user belongs to any of the required groups
            user_groups = request.user.groups.values_list('name', flat=True)
            if any(group in user_groups for group in group_names):
                return view_func(request, *args, **kwargs)

            # Permission denied - redirect to previous page or home
            messages.error(request, 'Ita la iha permisaun atu asesu pájina ne\'e!')
            referer = request.META.get('HTTP_REFERER')
            if referer:
                return redirect(referer)
            return redirect('main:home')

        return wrapper
    return decorator
