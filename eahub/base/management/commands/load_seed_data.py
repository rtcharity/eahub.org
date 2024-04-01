from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from eahub.config.settings import DjangoEnv


import environ


class Command(BaseCommand):
    help = 'Loads seed data into test and local database'

    def handle(self, *args, **kwargs):
        env = environ.Env().get_value("DJANGO_ENV", DjangoEnv, default=DjangoEnv.LOCAL)

        if env == DjangoEnv.LOCAL or env == DjangoEnv.E2E:
            socialApp = SocialApp(provider="google")
            socialApp.save()
            socialApp.sites.set([Sites.objects.first()])

