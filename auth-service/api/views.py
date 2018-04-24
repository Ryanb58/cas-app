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

import sys
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect

from django.utils.six.moves import urllib_parse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import (
    logout as auth_logout,
    login as auth_login,
    authenticate
)
from api.authentication import RefreshToken
from django_cas_ng.views import clean_sessions

from django_cas_ng.models import SessionTicket

from django_cas_ng.utils import (get_cas_client, get_service_url,
                    get_protocol, get_redirect_url,
                    get_user_from_session)

from django.contrib import messages
from django.utils.six import text_type


@csrf_exempt
@require_http_methods(["GET", "POST"])
def login(request, next_page=None, required=False):
    """Forwards to CAS login URL or verifies CAS ticket"""
    service_url = get_service_url(request, next_page)
    client = get_cas_client(service_url=service_url, request=request)

    if not next_page and settings.CAS_STORE_NEXT and 'CASNEXT' in request.session:
        next_page = request.session['CASNEXT']
        del request.session['CASNEXT']

    if not next_page:
        next_page = get_redirect_url(request)

    if request.method == 'POST' and request.POST.get('logoutRequest'):
        clean_sessions(client, request)
        return HttpResponseRedirect(next_page)

    # backward compability for django < 2.0
    is_user_authenticated = False

    if sys.version_info >= (3, 0):
        bool_type = bool
    else:
        bool_type = types.BooleanType

    if isinstance(request.user.is_authenticated, bool_type):
        is_user_authenticated = request.user.is_authenticated
    else:
        is_user_authenticated = request.user.is_authenticated()

    if is_user_authenticated:
        if settings.CAS_LOGGED_MSG is not None:
            message = settings.CAS_LOGGED_MSG % request.user.get_username()
            messages.success(request, message)
        return HttpResponseRedirect(next_page)

    ticket = request.GET.get('ticket')
    if ticket:
        user = authenticate(ticket=ticket,
                            service=service_url,
                            request=request)
        pgtiou = request.session.get("pgtiou")
        if user is not None:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            auth_login(request, user)
            SessionTicket.objects.create(
                session_key=request.session.session_key,
                ticket=ticket
            )

            # Set cookie.

            if pgtiou and settings.CAS_PROXY_CALLBACK:
                # Delete old PGT
                ProxyGrantingTicket.objects.filter(
                    user=user,
                    session_key=request.session.session_key
                ).delete()
                # Set new PGT ticket
                try:
                    pgt = ProxyGrantingTicket.objects.get(pgtiou=pgtiou)
                    pgt.user = user
                    pgt.session_key = request.session.session_key
                    pgt.save()
                except ProxyGrantingTicket.DoesNotExist:
                    pass

            if settings.CAS_LOGIN_MSG is not None:
                name = user.get_username()
                message = settings.CAS_LOGIN_MSG % name
                messages.success(request, message)

            # Get the response we are about to return.
            response = HttpResponseRedirect(next_page)

            # Set the cookie to the JWT.
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': text_type(refresh),
                'access': text_type(refresh.access_token),
            }
            response.set_cookie('auth_jwt', data['access'])
            return response

        elif settings.CAS_RETRY_LOGIN or required:
            return HttpResponseRedirect(client.get_login_url())
        else:
            raise PermissionDenied(_('Login failed.'))
    else:
        if settings.CAS_STORE_NEXT:
            request.session['CASNEXT'] = next_page
        return HttpResponseRedirect(client.get_login_url())

from django.contrib.auth import logout


@require_http_methods(["GET"])
def logout(request, next_page=None):
    if not next_page:
        next_page = request.GET.get('next')
    #response = django_cas_ng.views.logout(request, next_page)
    response = HttpResponseRedirect(next_page)
    response.delete_cookie('auth_jwt')
    response.delete_cookie(settings.SESSION_COOKIE_NAME)
    return response
