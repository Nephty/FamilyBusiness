from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _


def admin_required(view_func):
    """
    Decorator that checks if user is logged in and has admin role
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')

        if not request.user.is_staff:
            messages.error(request, _("admin_access_required"))
            return redirect('home:home')

        return view_func(request, *args, **kwargs)

    return _wrapped_view