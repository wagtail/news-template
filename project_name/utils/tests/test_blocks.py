from pathlib import Path

from django.test import SimpleTestCase
from wagtail import blocks

from {{ project_name }}.utils.blocks import CTABlock, CTASectionBlock, LinkStreamBlock, StoryBlock


OPEN_BLOCK = "{% templatetag openblock %}"
CLOSE_BLOCK = "{% templatetag closeblock %}"
OPEN_VARIABLE = "{% templatetag openvariable %}"
CLOSE_VARIABLE = "{% templatetag closevariable %}"


class CTABlockTests(SimpleTestCase):
    def setUp(self):
        self.block = CTABlock()

    def test_cta_block_imports_with_backwards_compatible_alias(self):
        self.assertIs(CTASectionBlock, CTABlock)

    def test_expected_fields_exist(self):
        self.assertEqual(
            list(self.block.child_blocks.keys()),
            ["title", "text", "button_text", "link"],
        )
        self.assertIsInstance(self.block.child_blocks["title"], blocks.CharBlock)
        self.assertIsInstance(self.block.child_blocks["text"], blocks.RichTextBlock)
        self.assertIsInstance(self.block.child_blocks["button_text"], blocks.CharBlock)
        self.assertIsInstance(self.block.child_blocks["link"], LinkStreamBlock)

    def test_button_text_is_independent_from_link_title(self):
        self.assertIn("button_text", self.block.child_blocks)
        self.assertNotEqual(
            self.block.child_blocks["button_text"], self.block.child_blocks["link"]
        )

    def test_link_stream_block_is_still_required_destination(self):
        link_block = self.block.child_blocks["link"]

        self.assertIsInstance(link_block, LinkStreamBlock)
        self.assertEqual(link_block.meta.min_num, 1)
        self.assertEqual(link_block.meta.max_num, 1)
        self.assertEqual(list(link_block.child_blocks.keys()), ["internal", "external"])

    def test_story_block_uses_cta_block_without_affecting_other_blocks(self):
        story_block = StoryBlock()

        self.assertIsInstance(story_block.child_blocks["cta"], CTABlock)
        self.assertEqual(
            list(story_block.child_blocks.keys()),
            ["section", "cta", "statistics"],
        )

    def test_cta_template_references_new_fields(self):
        template = Path(
            "templates/components/streamfield/blocks/cta_block.html"
        ).read_text()

        self.assertIn(f"{OPEN_VARIABLE} value.title {CLOSE_VARIABLE}", template)
        self.assertIn(f"{OPEN_VARIABLE} value.text|richtext {CLOSE_VARIABLE}", template)
        self.assertIn("title=value.button_text", template)
        self.assertIn(
            f"{OPEN_BLOCK} with cta_link=value.link.0 {CLOSE_BLOCK}", template
        )
        self.assertNotIn(f"{OPEN_VARIABLE} value.heading {CLOSE_VARIABLE}", template)
        self.assertNotIn(
            f"{OPEN_VARIABLE} value.description {CLOSE_VARIABLE}", template
        )
        self.assertNotIn("cta_link.value.get_title", template)
