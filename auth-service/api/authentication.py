import re
import requests

from os.path import join as pathjoin

import cas

from lxml import etree

from django.utils.functional import cached_property
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken as BaseRefreshToken
from rest_framework_simplejwt.models import TokenUser as BaseTokenUser
from rest_framework_simplejwt.authentication \
    import JWTTokenUserAuthentication as BaseJWTTokenUserAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken

from main.models import Realm, ExternalAuthentication, Organization


TICKET_RE = re.compile('ticket=([\w-]+)')
User = get_user_model()


def get_cas_client(server_url, service_url):
    client = cas.CASClient(
        service_url=service_url,
        version=settings.CAS_VERSION,
        server_url=server_url,
        extra_login_params=settings.CAS_EXTRA_LOGIN_PARAMS,
        renew=settings.CAS_RENEW,
        username_attribute=settings.CAS_USERNAME_ATTRIBUTE,
        proxy_callback=settings.CAS_PROXY_CALLBACK,
    )
    return client


def get_realm_and_org(orgname):
    realm, organization = None, None
    try:
        organization = Organization.objects.get(name=orgname)
        realm = organization.realm
    except Organization.DoesNotExist:
        realm = Realm.objects.default()

    return realm, organization


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


class BaseExternalBackend(ModelBackend):
    TYPE = None

    def _authenticate(self, *args, **kwargs):
        raise NotImplementedError()

    def authenticate(self, request, orgname=None, **kwargs):
        realm, organization = get_realm_and_org(orgname)

        # If realm does not support this type of authentication, bail out.
        auth_methods = realm.auth_methods.filter(auth_type=self.TYPE)
        
        if len(auth_methods) == 0:
            return

        for auth_method in auth_methods:
            user = self._authenticate(
                realm, organization, auth_method, **kwargs)

            if user is not None:
                return user


class CASTicketBackend(BaseExternalBackend):
    TYPE = ExternalAuthentication.AUTH_TYPE_CAS

    def _authenticate(self, realm, organization, auth_method, ticket=None,
                      service=None):
        client = get_cas_client(auth_method.url, service)
        username, attributes, pgtiou = client.verify_ticket(ticket)

        if not username:
            return

        # Create shadow user:
        organization = Organization.objects.get(realm=realm)
        user, created = User.objects.get_or_create(
            realm=realm, organization=organization, username=username)

        for attr in ('email', ):
            setattr(user, attr, attributes[attr])
        user.save()

        if created:
            user.auth_method = auth_method

        return user


class CASPostBackend(CASTicketBackend):
    TYPE = ExternalAuthentication.AUTH_TYPE_CAS

    def _authenticate(self, realm, organization, auth_method, username=None,
                      password=None, service=None):
        s = requests.session()
        url = pathjoin(auth_method.url, 'login')

        r = s.get(url, params={'service': service})
        if r.status_code != 200:
            return

        csrftoken = s.cookies['csrftoken']
        payload = {
            'csrfmiddlewaretoken': csrftoken,
            'username': username,
            'password': password,
        }

        r = s.post(url, data=payload, params={'service': service},
                   allow_redirects=False)
        if r.status_code not in (301, 302):
            return

        ticket = r.headers['Location']
        ticket = TICKET_RE.search(ticket)

        if ticket is None:
            return
        
        ticket = ticket.groups()[0]

        return super()._authenticate(
            realm, organization, auth_method, ticket=ticket, service=service)


class DatabaseBackend(object):
    def authenticate(self, request, orgname=None, username=None, password=None):
        realm, organization = get_realm_and_org(orgname)

        try:
            # Get a user from the site with matching username, but only if the
            # auth_method for that user is None (internal).
            user = User.objects.get(
                realm=realm, auth_method=None, username=username)
        except User.DoesNotExist:
            return

        if not user.check_password(password):
            return

        return user


class JWTTokenUserAuthentication(BaseJWTTokenUserAuthentication):
    """
    Returns an extended TokenUser instance.

    Used with Django Rest Framework.
    """

    def get_user(self, validated_token):
        if api_settings.USER_ID_CLAIM not in validated_token:
            raise InvalidToken(
                _('Token contained no recognizable user identification'))

        try:
            return User.objects.get(id=validated_token.get('user_id', None))
        except User.DoesNotExist:
            return
