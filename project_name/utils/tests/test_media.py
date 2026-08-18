from django.test import SimpleTestCase
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from ..blocks import CaptionedImageBlock, MediaBlock


class MediaBlockTests(SimpleTestCase):
    def test_media_block_can_be_imported_from_shared_blocks_package(self):
        self.assertIsSubclass(MediaBlock, blocks.StructBlock)

    def test_media_block_has_intended_fields(self):
        block = MediaBlock()

        self.assertEqual(list(block.child_blocks), ["image", "image_alt_text", "caption"])
        self.assertIsInstance(block.child_blocks["image"], ImageChooserBlock)
        self.assertIsInstance(block.child_blocks["image_alt_text"], blocks.CharBlock)
        self.assertFalse(block.child_blocks["image_alt_text"].required)
        self.assertIsInstance(block.child_blocks["caption"], blocks.CharBlock)
        self.assertFalse(block.child_blocks["caption"].required)

    def test_media_block_uses_existing_image_template(self):
        self.assertEqual(
            MediaBlock().meta.template,
            "components/streamfield/blocks/image_block.html",
        )

    def test_media_block_is_not_coupled_to_page_specific_struct_value(self):
        self.assertIs(MediaBlock().meta.value_class, blocks.StructValue)

    def test_captioned_image_block_retains_existing_media_functionality(self):
        self.assertIsSubclass(CaptionedImageBlock, MediaBlock)
        self.assertEqual(
            CaptionedImageBlock().meta.template,
            "components/streamfield/blocks/image_block.html",
        )
