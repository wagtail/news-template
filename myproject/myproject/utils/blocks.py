from collections import defaultdict

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from myproject.utils.struct_values import CardStructValue, LinkStructValue


class AccordionBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    content = blocks.RichTextBlock()

    class Meta:
        label = "Section"
        icon = "title"


class AccordionBlock(blocks.StructBlock):
    heading = blocks.ListBlock(AccordionBlock())
    list = blocks.ListBlock(AccordionBlock())

    class Meta:
        icon = "list-ol"
        template = "components/accordion/accordion.html"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    image_alt_text = blocks.CharBlock(
        required=False,
        help_text="If left blank, the image's global alt text will be used.",
    )
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "components/streamfield/blocks/image_block.html"


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


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(form_classname="title")
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "components/streamfield/blocks/quote_block.html"


class CardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock(required=False, features=["bold", "italic"])
    link = LinkStreamBlock(required=False, min_num=0)

    class Meta:
        icon = "form"
        template = "components/streamfield/blocks/card_block.html"
        label = "Card"
        value_class = CardStructValue


class FeaturedArticleBlock(blocks.StructBlock):
    link = ArticlePageLinkBlock()
    image = ImageChooserBlock(
        required=False,
        help_text="Set to override the image of the chosen article page.",
    )
    description = blocks.TextBlock(
        max_length=255,
        required=False,
        help_text="Choose to override a page's listing summary or introduction.",
    )
    cta_text = blocks.CharBlock(
        max_length=255,
        blank=False,
        help_text="This is the cta link text. This will automatically redirect to the article page.",
    )
    left_aligned = blocks.BooleanBlock(
        required=False,
        help_text="If checked, the text will be left-aligned.",
    )

    class Meta:
        icon = "doc-full"
        template = "components/streamfield/blocks/feature_block.html"


class BaseSectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        icon="title",
        required=True
    )  # Should use H2s only
    sr_only_label = blocks.BooleanBlock(
        required=False,
        label="Screen reader only label",
        help_text="If checked, the heading will be hidden from view and avaliable to screen-readers only.",
    )

    class Meta:
        abstract = True
        icon = "title"


class StatisticSectionBlock(BaseSectionBlock):
    statistics = blocks.ListBlock(
        SnippetChooserBlock(
            "utils.Statistic"
        ),
        max_num=3,
        min_num=3,
    )

    class Meta:
        icon = "snippet"
        template = "components/streamfield/blocks/stat_block.html"


class CTASectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        icon="title",
        required=True
    )
    link = LinkStreamBlock()
    description = blocks.TextBlock(required=False)

    class Meta:
        icon = "link"
        label = "CTA"
        template = "components/streamfield/blocks/cta_block.html"


class BaseCardSectionBlock(BaseSectionBlock):
    cards = blocks.ListBlock(
        CardBlock(),
        max_num=6,
        min_num=3,
        label="Card",
    )
    class Meta:
        abstract = True
        icon = "form"


class CardSectionBlock(BaseCardSectionBlock):
    class Meta:
        template = "components/streamfield/blocks/card_section_block.html"


class PlainCardSectionBlock(BaseCardSectionBlock):
    class Meta:
        icon = "doc-full"
        template = "components/streamfield/blocks/plain_cards_block.html"


class SectionBlocks(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ol", "ul", "h3"],
        template="components/streamfield/blocks/paragraph_block.html",
    )


class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        icon="title",
        template="components/streamfield/blocks/heading2_block.html",
    )
    content = SectionBlocks()

    class Meta:
        icon = "doc-full"
        template = "components/streamfield/blocks/section_block.html"


class StoryBlock(blocks.StreamBlock):
    section = SectionBlock()
    cta = CTASectionBlock()
    statistics = StatisticSectionBlock()

    class Meta:
        template = "components/streamfield/stream_block.html"
