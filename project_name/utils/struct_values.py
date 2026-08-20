from django.template.defaultfilters import filesizeformat
from wagtail import blocks


class LinkStructValue(blocks.StructValue):
    def get_url(self) -> str:
        if link := self.get("link"):
            return link

        if page := self.get("page"):
            return page.url

        if document := self.get("document"):
            return document.url

        return ""

    def get_title(self) -> str:
        if title := self.get("title"):
            return title

        if page := self.get("page"):
            page = page.specific

            return page.listing_title or page.title

        if document := self.get("document"):
            return document.title

        return ""

    def get_link_type(self) -> str:
        if self.get("page"):
            return "internal"
        if self.get("document"):
            return "document"
        return "external"

    def get_file_size(self) -> str:
        if document := self.get("document"):
            return filesizeformat(document.file.size)
        return ""

    def get_extension_type(self) -> str:
        if document := self.get("document"):
            return document.file_extension.upper()
        return ""
