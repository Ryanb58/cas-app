import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


DEFAULT_REALM_ID = '17a21472-c8ff-4fab-a8ce-56dfba40c423'
DEFAULT_ORGANIZATION_ID = '18b66bec-1a7a-48ff-b517-28ac7762ff1a'


class RealmManager(models.Manager):
    def default(self):
        return self.get(pk=DEFAULT_REALM_ID)

    def get_realm_or_default(self, realm_name):
        try:
            return self.get(name=realm_name)
        except self.model.DoesNotExist:
            return self.default()


class Realm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

    objects = RealmManager()


class ExternalAuthentication(models.Model):
    AUTH_TYPE_CAS = 1
    AUTH_TYPES = {
        AUTH_TYPE_CAS: 'CAS',
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    realm = models.ForeignKey(Realm, related_name='auth_methods')
    auth_type = models.IntegerField(choices=AUTH_TYPES.items())
    url = models.URLField()


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    realm = models.ForeignKey(Realm, default=DEFAULT_REALM_ID)


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=80, unique=True)


class User(AbstractUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'organization_id']

    class Meta:
        unique_together = ('realm', 'username')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    realm = models.ForeignKey(Realm, default=DEFAULT_REALM_ID)
    organization = models.ForeignKey(Organization)
    auth_method = models.ForeignKey(ExternalAuthentication, null=True)
    groups = models.ManyToManyField(Group, related_name='users')
    username = models.CharField(
        _('username'),
        max_length=150,
        # Unique by realm.
        # unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )