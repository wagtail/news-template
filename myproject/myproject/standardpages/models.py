from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index

from wagtail.fields import StreamField
from myproject.utils.blocks import StoryBlock
from myproject.utils.models import BasePage


class StandardPage(BasePage):
    template = "pages/standard_page.html"

    introduction = models.TextField(blank=True)
    display_table_of_contents = models.BooleanField(default=True)
    body = StreamField(StoryBlock())
    featured_section_title = models.TextField(blank=True)

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("display_table_of_contents"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("featured_section_title", heading="Title"),
                InlinePanel(
                    "page_related_pages",
                    label="Pages",
                    max_num=3,
                ),
            ],
            heading="Featured section",
        ),
    ]


class IndexPage(BasePage):
    template = "pages/index_page.html"

    introduction = RichTextField(blank=True)
    body = StreamField(StoryBlock(), blank=True)

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        InlinePanel(
            "page_related_pages",
            label="Featured pages",
            min_num=3,
            max_num=12,
        ),
        FieldPanel("body")
    ]

