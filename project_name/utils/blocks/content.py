from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock, ImageBlock

from .links import ArticlePageLinkBlock, LinkStreamBlock
from ..struct_values import CardStructValue


class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    image_alt_text = blocks.CharBlock(
        required=False,
        help_text="If left blank, the image's global alt text will be used.",
    )
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "components/streamfield/blocks/image_block.html"


class AccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    content = blocks.RichTextBlock()

    class Meta:
        label = "Accordion item"
        icon = "title"


class AccordionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    list = blocks.ListBlock(AccordionItemBlock())

    class Meta:
        icon = "list-ol"
        template = "components/streamfield/blocks/accordion.html"


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
    image = ImageBlock(
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
