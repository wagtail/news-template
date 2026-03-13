from django.db import models
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.snippets.blocks import SnippetChooserBlock

from myproject.utils.blocks import LinkStreamBlock, InternalLinkBlock


@register_setting(icon="list-ul")
class NavigationSettings(BaseSiteSetting, ClusterableModel):
    primary_navigation = StreamField(
        [("link", InternalLinkBlock())],
        blank=True,
        help_text="Main site navigation",
        
    )
    footer_navigation = StreamField(
        [("link_section", blocks.StructBlock([
                ("section_heading", blocks.CharBlock()),
                ("links", LinkStreamBlock(
                    label = "Links", 
                    max_num = None
                )),
            ])) 
        ],
        blank=True,
    )

    panels = [
        FieldPanel("primary_navigation"),
        FieldPanel("footer_navigation"),
    ]
