from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from rest_framework_simplejwt.authentication \
    import JWTTokenUserAuthentication as BaseJWTTokenUserAuthentication
from rest_framework_simplejwt.models import TokenUser as BaseTokenUser
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken as BaseRefreshToken


class RefreshToken(BaseRefreshToken):
    """
    Token that includes additional fields.
    """

    @classmethod
    def for_user(cls, user):
        """Add additional fields to JWT."""
        token = super().for_user(user)
        token['username'] = user.username
        return token


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
                _('Toiken contained no recognizable user identification'))

        return TokenUser(validated_token)
