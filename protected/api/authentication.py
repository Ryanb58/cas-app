from django.utils.six import text_type

from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from rest_framework import HTTP_HEADER_ENCODING

from rest_framework_simplejwt.authentication \
    import JWTTokenUserAuthentication as BaseJWTTokenUserAuthentication
from rest_framework_simplejwt.models import TokenUser as BaseTokenUser
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken


COOKIE_NAME = 'auth_jwt'


class TokenUser(BaseTokenUser):
    """
    Extended TokenUser that contains username.
    """

    @cached_property
    def username(self):
        return self.token.get('username', None)


class JWTTokenUserAuthentication(BaseJWTTokenUserAuthentication):
    """
    Returns an extended TokenUser instance.

    Used with Django Rest Framework.
    """

    def get_user(self, validated_token):
        if api_settings.USER_ID_CLAIM not in validated_token:
            raise InvalidToken(
                _('Token contained no recognizable user identification'))

        return TokenUser(validated_token)

    def get_header(self, request):
        """Checks header and cookie for auth."""
        header = super().get_header(request)

        if header:
            return header

        # Check the cookie...
        cookie = request.COOKIES.get(COOKIE_NAME, None)

        if cookie:
            header = 'Bearer %s' % cookie

            if isinstance(header, text_type):
                # Work around django test client oddness
                header = header.encode(HTTP_HEADER_ENCODING)

            return header
