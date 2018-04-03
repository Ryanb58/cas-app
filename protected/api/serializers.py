from rest_framework import serializers

from rest_framework_simplejwt.serializers \
    import TokenObtainPairSerializer as BaseTokenObtainPairSerializer

from api.auth import RefreshToken


class TokenUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

   