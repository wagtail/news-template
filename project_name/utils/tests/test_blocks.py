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

        self.assertEqual(list(block.child_blocks.keys()), ["title", "text", "button"])
        self.assertIsInstance(block.child_blocks["button"], LinkStreamBlock)
        self.assertNotIn("button_text", block.child_blocks)
        self.assertNotIn("link", block.child_blocks)

    def test_story_block_uses_call_to_action_block(self):
        story_block = StoryBlock()

        self.assertIsInstance(story_block.child_blocks["cta"], CallToActionBlock)

    def test_cta_template_references_block_and_button_fields(self):
        template = Path(
            "templates/components/streamfield/blocks/cta_block.html"
        ).read_text()

        self.assertIn(f"{OPEN_VARIABLE} value.title {CLOSE_VARIABLE}", template)
        self.assertIn(f"{OPEN_VARIABLE} value.text|richtext {CLOSE_VARIABLE}", template)
        self.assertIn(
            f"{OPEN_BLOCK} with cta_button=value.button.0 {CLOSE_BLOCK}", template
        )
        self.assertIn("title=cta_button.value.get_title", template)
        self.assertIn("url=cta_button.value.get_url", template)
        self.assertNotIn("button_text", template)
        self.assertNotIn("value.link", template)
