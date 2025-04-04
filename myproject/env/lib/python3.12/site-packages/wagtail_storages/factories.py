from wagtail.documents import get_document_model
from wagtail.models import Collection, CollectionViewRestriction

import factory
import factory.django

Document = get_document_model()


class DocumentFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: "Document" + str(n))
    file = factory.django.FileField(
        filename="testfile.txt",
        data=b"Test document",
    )
    collection = factory.SubFactory("wagtail_storages.factories.CollectionFactory")

    class Meta:
        model = Document


class CollectionFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Collection" + str(n))
    depth = 0

    class Meta:
        model = Collection

    @classmethod
    def _create(cls, model_class, parent_collection=None, *args, **kwargs):
        if parent_collection is None:
            # Use root collection as a default.
            parent_collection = Collection.get_first_root_node()
        collection = model_class(*args, **kwargs)
        parent_collection.add_child(instance=collection)
        return collection


class CollectionViewRestrictionFactory(factory.django.DjangoModelFactory):
    collection = factory.SubFactory(CollectionFactory)
    restriction_type = CollectionViewRestriction.PASSWORD
    password = "password"

    class Meta:
        model = CollectionViewRestriction
