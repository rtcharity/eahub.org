from azure.storage.blob.baseblobservice import BaseBlobService
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates the Azure Blob Storage container used to store media"

    def handle(self, *args, **options):
        BaseBlobService(
            connection_string=settings.AZURE_CONNECTION_STRING
        ).create_container(settings.AZURE_CONTAINER)
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created container "{settings.AZURE_CONTAINER}"'
            )
        )
