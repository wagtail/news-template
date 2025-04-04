import logging

from django.conf import settings
from django.core.files.storage import default_storage

from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.documents import get_document_model
from wagtail.models import Site

import storages.backends.s3boto3

logger = logging.getLogger(__name__)


def update_document_acl(document):
    acl = get_acl_for_collection(document.collection)
    document.file.file.obj.Acl().put(ACL=acl)
    logger.debug('Set document ACL to "%s" on "%s"', acl, document.file.name)


def update_collection_document_acls(collection):
    acl = get_acl_for_collection(collection)
    documents = get_document_model().objects.filter(collection=collection)
    for document in documents:
        logger.debug(
            'Set document ACL to "%s" on "%s"',
            acl,
            document.file.name,
        )
        document.file.file.obj.Acl().put(ACL=acl)


def get_acl_for_collection(collection):
    if collection.get_view_restrictions():
        return "private"
    return "public-read"


def build_absolute_url_for_site_for_path(site, path):
    return "{}{}".format(site.root_url.rstrip("/"), path)


def build_absolute_urls_for_all_sites_for_path(path):
    for site in Site.objects.all():
        yield build_absolute_url_for_site_for_path(site, path)


def is_s3_boto3_storage_used():
    return issubclass(
        default_storage.__class__,
        storages.backends.s3boto3.S3Boto3Storage,
    )


def get_frontend_cache_configuration():
    return getattr(settings, "WAGTAIL_STORAGES_DOCUMENTS_FRONTENDCACHE", {})


def purge_document_from_cache(document):
    # No need for check if they are public or private - if they've changed,
    # they should be out of cache.
    logger.debug('Purge document "%s" from the front-end cache', document.file.name)
    frontend_cache_configuration = get_frontend_cache_configuration()
    if frontend_cache_configuration:
        s3_batch = PurgeBatch()
        s3_batch.add_url(document.file.url)
        s3_batch.purge(backend_settings=frontend_cache_configuration)
    # Purge Wagtail document view URLs using normal site's cache.
    wagtail_batch = PurgeBatch()
    wagtail_batch.add_urls(build_absolute_urls_for_all_sites_for_path(document.url))
    wagtail_batch.purge()


def purge_collection_documents_from_cache(collection):
    # Do not purge documents if they are in a public collection. Documents
    # themselves have not changed so no need to make redundant calls for big
    # collections.
    if not collection.get_view_restrictions():
        return
    logger.debug(
        'Purge documents of collection "%s" from the front-end cache',
        collection.name,
    )
    # Purge download URLs and actual files if they possibly used to be public.
    wagtail_batch = PurgeBatch()
    s3_batch = PurgeBatch()
    for document in get_document_model().objects.filter(collection=collection):
        wagtail_batch.add_urls(build_absolute_urls_for_all_sites_for_path(document.url))
        s3_batch.add_url(document.file.url)
    wagtail_batch.purge()
    frontend_cache_configuration = get_frontend_cache_configuration()
    if frontend_cache_configuration:
        s3_batch.purge(backend_settings=frontend_cache_configuration)
