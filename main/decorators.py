from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url='/auth/',  # not actually login, main page
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def superuser_only(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,
        login_url='/',  # not actually login, main page
        redirect_field_name=None,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def writer_only(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_writer or u.is_superuser),
        login_url='/',  # not actually login, main page
        redirect_field_name=None,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
