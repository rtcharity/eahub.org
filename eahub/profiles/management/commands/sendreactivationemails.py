import sys
from email import utils as email_utils

from allauth.account import forms
from allauth.account import utils as account_utils
from django.conf import settings
from django.contrib.sites import shortcuts
from django.core import mail
from django.core.management import base
from django.db import models
from django.template import loader

from ... import models as profiles_models

EMEA_COUNTRIES = [
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Armenia",
    "Austria",
    "Azerbaijan",
    "Bahrain",
    "Belarus",
    "Belgium",
    "Benin",
    "Bosnia and Herzegovina",
    "Botswana",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cameroon",
    "Cape Verde",
    "Central African Republic",
    "Chad",
    "Comoros",
    "Congo - Brazzaville",
    "Congo - Kinshasa",
    "Cote d'Ivoire",
    "Croatia",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "East Germany",
    "Egypt",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Ethiopia",
    "Faroe Islands",
    "Finland",
    "France",
    "French Southern Territories",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Guernsey",
    "Guinea",
    "Guinea-Bissau",
    "Hungary",
    "Iceland",
    "Iraq",
    "Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jersey",
    "Jordan",
    "Kenya",
    "Kuwait",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macedonia",
    "Madagascar",
    "Malawi",
    "Mali",
    "Malta",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Metropolitan France",
    "Moldova",
    "Monaco",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Namibia",
    "Netherlands",
    "Neutral Zone",
    "Niger",
    "Nigeria",
    "Norway",
    "Oman",
    "Palestinian Territories",
    "People's Democratic Republic of Yemen",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Réunion",
    "Saint Helena",
    "Saint Pierre and Miquelon",
    "San Marino",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Serbia and Montenegro",
    "Seychelles",
    "Sierra Leone",
    "Slovakia",
    "Slovenia",
    "Somalia",
    "South Africa",
    "South Georgia and the South Sandwich Islands",
    "Spain",
    "Sudan",
    "Svalbard and Jan Mayen",
    "Swaziland",
    "Sweden",
    "Switzerland",
    "Syria",
    "São Tomé and Príncipe",
    "Tanzania",
    "Togo",
    "Tunisia",
    "Turkey",
    "UK",
    "Uganda",
    "Ukraine",
    "Union of Soviet Socialist Republics",
    "United Arab Emirates",
    "United Kingdom",
    "Vatican City",
    "Western Sahara",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]


class Command(base.BaseCommand):
    help = "Send reactivation to legacy Hub users who haven't signed in"

    def add_arguments(self, parser):
        parser.add_argument("phase", choices=["phase1", "phase2", "phase3", "phase4"])

    def handle(self, *args, **options):
        tester_emails = sys.stdin.read().splitlines()
        profiles = (
            profiles_models.Profile.objects.select_related("user")
            .filter(user__password="", user__is_active=True)
            .annotate(canary_bucket=(models.F("pk") % 10))
        )
        is_tester = models.Q(user__email__in=tester_emails)
        is_emea = models.Q(country__in=EMEA_COUNTRIES)
        is_canary = models.Q(canary_bucket=0)
        phase = options["phase"]
        if phase == "phase1":
            profiles = profiles.filter(is_tester)
        elif phase == "phase2":
            profiles = profiles.filter(~is_tester, is_emea, is_canary)
        elif phase == "phase3":
            profiles = profiles.filter(~is_tester, is_emea, ~is_canary)
        elif phase == "phase4":
            profiles = profiles.filter(~is_tester, ~is_emea)
        token_generator = forms.EmailAwarePasswordResetTokenGenerator()
        common_context = {
            "protocol": settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL,
            "domain": shortcuts.get_current_site(request=None).domain,
        }
        messages = []
        for profile in profiles:
            user = profile.user
            context = {
                "profile": profile,
                "uidb36": account_utils.user_pk_to_url_str(user),
                "key": token_generator.make_token(user),
                **common_context,
            }
            message = mail.EmailMultiAlternatives(
                subject="Announcing the EA Hub 2.0",
                body=loader.render_to_string("emails/reactivate.txt", context),
                from_email="Michael from LEAN <contact@eahub.org>",
                to=[email_utils.formataddr((profile.get_full_name(), user.email))],
            )
            message.attach_alternative(
                loader.render_to_string("emails/reactivate.html", context), "text/html"
            )
            messages.append(message)
        mail.get_connection().send_messages(messages)
