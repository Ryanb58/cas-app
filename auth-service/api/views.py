from django.shortcuts import render
from django.contrib.auth import get_user_model

import django_cas_ng.views
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.views \
    import TokenObtainPairView as BaseTokenObtainPairView

from api.serializers import TokenObtainPairSerializer
from api.serializers import RealmSerializer
from api.serializers import OrganizationSerializer
from api.serializers import UserSerializer
from api.serializers import GroupSerializer
from api.serializers import ExternalAuthenticationSerializer

from main.models import Organization, Realm, ExternalAuthentication, Group


User = get_user_model()


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RealmViewSet(viewsets.ModelViewSet):
    serializer_class = RealmSerializer
    queryset = Realm.objects.all()
    permission_classes = [IsAdminUser]


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    permission_classes = [IsAdminUser]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            organization=self.request.user.organization)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(
            organization=self.request.user.organization)


class ExternalAuthenticationViewSet(viewsets.ModelViewSet):
    serializer_class = ExternalAuthenticationSerializer
    queryset = ExternalAuthentication.objects.all()
    permission_classes = [IsAdminUser]


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login(request, next_page=None, required=False):
    from ipdb import set_trace;set_trace()
    return django_cas_ng.views.login(
        request, next_page=next_page, required=required)
