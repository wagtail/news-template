from PIL import ImageOps
from django.db import models
from wagtail import hooks
from wagtail.search import index
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.images.image_operations import FilterOperation


class CustomImage(AbstractImage):
    admin_form_fields = Image.admin_form_fields

    search_fields = AbstractImage.search_fields + [index.SearchField("description")]


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        "CustomImage", related_name="renditions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)

    @property
    def object_position_style(self):
        """
        Returns a `object-position` rule to add to an img element's inline style attribute.

        Similar code is used for wagtail image's background_position_style method.
        Reference: https://github.com/wagtail/wagtail/blob/845a2acb365241643c2f453e4b962a586ae5e713/wagtail/images/models.py#L1229
        """
        focal_point = self.focal_point
        if focal_point:
            horz = int((focal_point.x * 100) // self.width)
            vert = int((focal_point.y * 100) // self.height)
            return f"object-position: {horz}% {vert}%;"
        else:
            return "object-position: 50% 50%;"


class GrayscaleOperation(FilterOperation):
    def construct(self):
        pass

    def run(self, willow, image, env):
        willow.image = ImageOps.grayscale(willow.image)
        return willow


@hooks.register("register_image_operations")
def register_image_operations():
    return [
        ("gray", GrayscaleOperation),
    ]
