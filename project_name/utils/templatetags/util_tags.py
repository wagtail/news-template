from django import template
from django.template.defaultfilters import slugify

register = template.Library()


@register.simple_tag
def format_heading_id(text, id) -> str:
    """Generate Unique IDs for page headings"""
    truncated_id = id[:8]
    formatted_text = f"{slugify(text)}-{truncated_id}"
    return formatted_text


# Table of contents
@register.filter(name="table_of_contents_array")
def table_of_contents_array(streamfield_content):
    h2_blocks = [
        (format_heading_id(block.value, block.id), block.value)
        for block in streamfield_content
        if block.block_type == "h2"
    ]
    return h2_blocks
