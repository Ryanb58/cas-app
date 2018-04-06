from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.serializers \
    import TokenObtainPairSerializer as BaseTokenObtainPairSerializer

from api.authentication import RefreshToken
from main.models import Realm
from main.models import Organization
from main.models import Group
from main.models import ExternalAuthentication


User = get_user_model()


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    organization = serializers.CharField(required=False)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)


class RealmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realm
        fields = ('name', )


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'realm')
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'organization')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'organization')


class ExternalAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalAuthentication
        fields = ('realm', 'url')
