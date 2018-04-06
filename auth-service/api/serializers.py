from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.six import text_type
from django.utils.translation import gettext_lazy as _

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

    def validate(self, attrs):
        self.user = authenticate(**{
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
            'service': 'http://localhost:8000/api/auth/',
        })

        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise serializers.ValidationError(
                _('No active account found with the given credentials'),
            )

        refresh = self.get_token(self.user)

        data = {
            'refresh': text_type(refresh),
            'access': text_type(refresh.access_token),
        }

        return data

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
