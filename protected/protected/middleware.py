from rest_framework_simplejwt.exceptions import InvalidToken
from api.authentication import JWTTokenUserAuthentication
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser


def get_user(request):
    """Gets user from cache or from jwt."""
    if not hasattr(request, '_cached_user'):
        auth = JWTTokenUserAuthentication()
        try:
            user = auth.authenticate(request)
        except InvalidToken:
            return AnonymousUser()
        if isinstance(user, tuple):
            user = user[0]
        if user:
            request._cached_user = user
        else:
            return AnonymousUser()
    return request._cached_user


class JWTAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.user = SimpleLazyObject(lambda: get_user(request))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response