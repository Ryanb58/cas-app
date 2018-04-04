from rest_framework_simplejwt.serializers \
    import TokenObtainPairSerializer as BaseTokenObtainPairSerializer

from api.authentication import RefreshToken


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

