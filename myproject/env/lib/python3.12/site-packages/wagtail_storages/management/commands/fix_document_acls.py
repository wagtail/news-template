from django.core.management.base import BaseCommand, CommandError

from wagtail.models import Collection

from wagtail_storages.utils import (
    is_s3_boto3_storage_used,
    update_collection_document_acls,
)


class Command(BaseCommand):
    help = "Fix documents' ACLs on S3 to match their collection settings"

    def handle(self, *args, **options):
        if not is_s3_boto3_storage_used():
            raise CommandError(
                "Your storage needs to be set to S3Boto3Storage in order to "
                "use this command."
            )
        for collection in Collection.objects.all():
            update_collection_document_acls(collection)
