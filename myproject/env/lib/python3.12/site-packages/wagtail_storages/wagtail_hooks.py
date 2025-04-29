import django

import wagtail
from wagtail.documents import get_document_model
from wagtail.hooks import register

from wagtail_storages import backends, utils

HOOK_ORDER = getattr(django.conf.settings, "WAGTAIL_STORAGES_DOCUMENT_HOOK_ORDER", 100)


@register("before_serve_document", order=HOOK_ORDER)
def serve_document_from_s3(document, request):
    # Skip this hook if not using django-storages boto3 backend.
    if not utils.is_s3_boto3_storage_used():
        return

    # Send document_served signal.
    wagtail.documents.models.document_served.send(
        sender=get_document_model(),
        instance=document,
        request=request,
    )

    # If document has restrictions, generate a signed URL, otherwise
    # return its public URL.
    if document.collection.get_view_restrictions():
        backend_class = backends.get_private_s3_boto3_document_storage_backend_class()
        backend = backend_class()
        content_disposition = f"attachment; filename={document.filename}"
        file_url = backend.url(
            document.file.name,
            # Add Content-Disposition header to avoid users seeing signed URLs
            # in their web browser address bar.
            parameters={"ResponseContentDisposition": content_disposition},
        )
    else:
        file_url = document.file.url

    # Generate redirect response and add never_cache headers.
    response = django.shortcuts.redirect(file_url)
    del response["Cache-control"]
    django.utils.cache.add_never_cache_headers(response)
    return response
