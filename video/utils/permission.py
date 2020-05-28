import functools

from django.shortcuts import redirect, reverse


def dashboard_auth(func):
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect("{}?next={}".format(reverse('dashboard:login'), request.path))
        elif not user.is_superuser:
            return redirect("{}?next={}".format(reverse('dashboard:logout'), request.path))

        return func(self, request, *args, **kwargs)
    return wrapper