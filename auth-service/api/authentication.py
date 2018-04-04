import re
import requests

from os.path import join as pathjoin

from lxml import etree

from django.utils.functional import cached_property
from django.conf import settings
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken as BaseRefreshToken
from rest_framework_simplejwt.models import TokenUser as BaseTokenUser


TICKET_RE = re.compile('ticket=([\w-]+)')


class TokenUser(BaseTokenUser):
    """
    Extended TokenUser that contains username.
    """

    @cached_property
    def username(self):
        return self.token.get('username', None)


def xml_to_dict(element_tree):
    """Traverse the given XML element tree to convert it into a dictionary.
 
    :param element_tree: An XML element tree
    :type element_tree: xml.etree.ElementTree
    :rtype: dict
    """
    def internal_iter(tree, accum):
        """Recursively iterate through the elements of the tree accumulating
        a dictionary result.
 
        :param tree: The XML element tree
        :type tree: xml.etree.ElementTree
        :param accum: Dictionary into which data is accumulated
        :type accum: dict
        :rtype: dict
        """
        if tree is None:
            return accum
 
        if tree.getchildren():
            accum[tree.tag] = {}
            for each in tree.getchildren():
                result = internal_iter(each, {})
                if each.tag in accum[tree.tag]:
                    if not isinstance(accum[tree.tag][each.tag], list):
                        accum[tree.tag][each.tag] = [
                            accum[tree.tag][each.tag]
                        ]
                    accum[tree.tag][each.tag].append(result[each.tag])
                else:
                    accum[tree.tag].update(result)
        else:
            accum[tree.tag] = tree.text
 
        return accum
 
    return internal_iter(element_tree, {})


def parse_xml(s):
    """
    Parse an XML tree from the given string, removing all
    of the included namespace strings.
    """
    ns = re.compile(r'^{.*?}')
    et = etree.fromstring(s)
    for elem in et.getiterator():
        elem.tag = ns.sub('', elem.tag)
    return et


class CAS3Client(object):
    def __init__(self, server_url, service_url):
        self.server_url = server_url
        self.service_url = service_url

    def login(self, username, password):
        s = requests.session()
        url = pathjoin(self.server_url, 'login')

        r = s.get(url, params={'service': self.service_url})
        csrftoken = s.cookies['csrftoken']

        payload = {
            'csrfmiddlewaretoken': csrftoken,
            'username': username,
            'password': password,
        }

        r = s.post(url, data=payload, params={'service': self.service_url},
                   allow_redirects=False)
        if r.status_code not in (301, 302):
            return

        ticket = r.headers['Location']
        ticket = TICKET_RE.search(ticket).groups()[0]

        payload = {
            'ticket': ticket,
            'service': self.service_url,
            'format': 'json',
        }
        r = s.get(pathjoin(self.server_url, 'p3/serviceValidate'),
                  params=payload)
        if r.status_code != 200:
            return

        d = xml_to_dict(parse_xml(r.text))

        token = {
            'user_id': None,
            'username': d['serviceResponse']['authenticationSuccess']['user'],
            'email': d['serviceResponse']['authenticationSuccess']['attributes']['email'],
        }

        return TokenUser(token)


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


class CASPostBackend(object):
    def authenticate(self, request, username=None, password=None):
        # If not credentials, nothing to do.
        if username is None or password is None:
            return

        server_url = getattr(settings, 'CAS_SERVER_URL', None)

        # If not CAS server, nothing to do.
        if server_url is None:
            return

        service_url = 'http://localhost:8001/'
        client = CAS3Client(server_url, service_url)
        user = client.login(username, password)

        # If no user, nothing to do.
        if user is None:
            return

        return user
