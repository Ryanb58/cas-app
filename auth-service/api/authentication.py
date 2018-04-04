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
