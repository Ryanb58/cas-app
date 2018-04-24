from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.exceptions import InvalidToken
from api.authentication import JWTTokenUserAuthentication
from django.contrib.auth.models import AnonymousUser


class JWTAuthBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        """Verifies the JWT via the header or cookie."""
        auth = JWTTokenUserAuthentication()
        try:
            user = auth.authenticate(request)
        except InvalidToken:
            return AnonymousUser()
        if isinstance(user, tuple):
            user = user[0]
        return user or AnonymousUser()
