from pathlib import Path

from django.test import SimpleTestCase

from {{ project_name }}.utils.blocks import CallToActionBlock, LinkStreamBlock, StoryBlock


OPEN_BLOCK = "{% templatetag openblock %}"
CLOSE_BLOCK = "{% templatetag closeblock %}"
OPEN_VARIABLE = "{% templatetag openvariable %}"
CLOSE_VARIABLE = "{% templatetag closevariable %}"


class CallToActionBlockTests(SimpleTestCase):
    def test_call_to_action_block_fields(self):
        block = CallToActionBlock()

        self.assertEqual(list(block.child_blocks.keys()), ["title", "text", "link"])
        self.assertIsInstance(block.child_blocks["link"], LinkStreamBlock)
        self.assertNotIn("button_text", block.child_blocks)

    def test_story_block_uses_call_to_action_block(self):
        story_block = StoryBlock()

        self.assertIsInstance(story_block.child_blocks["cta"], CallToActionBlock)

    def test_cta_template_references_block_and_link_fields(self):
        template = Path(
            "templates/components/streamfield/blocks/cta_block.html"
        ).read_text()

        self.assertIn(f"{OPEN_VARIABLE} value.title {CLOSE_VARIABLE}", template)
        self.assertIn(f"{OPEN_VARIABLE} value.text|richtext {CLOSE_VARIABLE}", template)
        self.assertIn(
            f"{OPEN_BLOCK} with cta_link=value.link.0 {CLOSE_BLOCK}", template
        )
        self.assertIn("title=cta_link.value.get_title", template)
        self.assertIn("url=cta_link.value.get_url", template)
        self.assertNotIn("button_text", template)
