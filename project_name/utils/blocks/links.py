from wagtail import blocks

from ..struct_values import LinkStructValue


class InternalLinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(
        required=False,
        help_text="Leave blank to use page's listing title.",
    )

    class Meta:
        icon = "link"
        value_class = LinkStructValue


class ArticlePageLinkBlock(InternalLinkBlock):
    page = blocks.PageChooserBlock(
        page_type="news.ArticlePage",
    )


class ExternalLinkBlock(blocks.StructBlock):
    link = blocks.URLBlock()
    title = blocks.CharBlock()

    class Meta:
        icon = "link"
        value_class = LinkStructValue


class LinkStreamBlock(blocks.StreamBlock):
    """
    StreamBlock that allows editors to add a single link of type internal or external.
    """

    internal = InternalLinkBlock()
    external = ExternalLinkBlock()

    class Meta:
        icon = "link"
        label = "Link"
        min_num = 1
        max_num = 1
