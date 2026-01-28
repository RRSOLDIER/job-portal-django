from django.shortcuts import redirect
from functools import wraps
from django.conf import settings


def recruiter_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        if request.user.userprofile.role != 'recruiter':
            return redirect(settings.LOGIN_URL)

        return view_func(request, *args, **kwargs)
    return wrapper


def candidate_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        if request.user.userprofile.role != 'candidate':
            return redirect(settings.LOGIN_URL)

        return view_func(request, *args, **kwargs)
    return wrapper
