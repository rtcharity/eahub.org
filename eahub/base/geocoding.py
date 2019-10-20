from django.conf import settings
from geopy import geocoders


class Geocoding:
    @staticmethod
    def geocode(city, country):
        if settings.GOOGLE_MAPS_API_KEY is None:
            return

        return geocoders.GoogleV3(timeout=10, api_key=None).geocode(
            f"{city}, {country}"
        )
