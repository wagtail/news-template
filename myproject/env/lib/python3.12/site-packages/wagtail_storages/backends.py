from storages.backends.s3boto3 import S3Boto3Storage


class PrivateS3Boto3StorageForWagtailDocument(S3Boto3Storage):
    # Enable signing.
    querystring_auth = True

    # Signing URLs does not work with custom domains.
    custom_domain = None


def get_private_s3_boto3_document_storage_backend_class():
    return PrivateS3Boto3StorageForWagtailDocument
