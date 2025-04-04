from wagtail import hooks
from wagtail.rich_text import LinkHandler


class ExternalLinkHandler(LinkHandler):
    identifier = "external"

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]

        return f'<a data-rich-text-external-link href="{href}">'


@hooks.register("register_rich_text_features")
def register_link_handler(features):
    features.register_link_type(ExternalLinkHandler)
