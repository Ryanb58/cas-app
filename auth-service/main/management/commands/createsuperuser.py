from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

from main.models import DEFAULT_ORGANIZATION_ID


class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        options['organization_id'] = DEFAULT_ORGANIZATION_ID
        super(Command, self).handle(*args, **options)
