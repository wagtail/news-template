from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from .links import LinkStreamBlock
from .content import CardBlock


class BaseSectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        icon="title",
        required=True
    )
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


class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        form_classname="title",
        icon="title",
        required=True
    )
    text = blocks.RichTextBlock(
        features=["bold", "italic", "link"],
        required=False,
    )
    button_text = blocks.CharBlock(required=True)
    link = LinkStreamBlock()

    class Meta:
        icon = "link"
        label = "CTA"
        template = "components/streamfield/blocks/cta_block.html"


CTASectionBlock=CTABlock

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
    cta = CallToActionBlock()
    statistics = StatisticSectionBlock()

    class Meta:
        template = "components/streamfield/stream_block.html"
