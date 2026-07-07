from django.db.models.functions import Coalesce
from django.urls import reverse
from django.contrib.syndication.views import Feed
from wagtail.models import Site

from {{ project_name }}.news.models import ArticlePage, NewsListingPage


class LatestArticlesFeed(Feed):
    """RSS 2.0 feed for public, published news articles."""

    @property
    def site(self):
        return Site.objects.filter(is_default_site=True).first()


    @property
    def news_listing(self):
        return NewsListingPage.objects.live().public().first()

    def get_object(self, request):
        self.request = request

    def title(self, obj):
        parts = []
        if self.site and self.site.site_name:
            parts.append(self.site.site_name)
        if self.news_listing and self.news_listing.title:
            parts.append(self.news_listing.title)
        return " – ".join(parts) or "News"

    def description(self, obj):
        if self.news_listing:
            return (
                self.news_listing.search_description
                or self.news_listing.listing_summary
                or self.news_listing.plain_introduction
                or f"Latest articles from {self.title(obj)}"
            )
        return f"Latest articles from {self.title(obj)}"

    def link(self, obj):
        if self.news_listing:
            return self.news_listing.get_full_url(self.request)
        return self.request.build_absolute_uri(reverse("news_feed"))

    def feed_url(self, obj):
        return self.request.build_absolute_uri(reverse("news_feed"))

    def items(self, obj):
        return (
            ArticlePage.objects.live()
            .public()
            .annotate(date=Coalesce("publication_date", "first_published_at"))
            .select_related("author", "topic")
            .order_by("-date")
        )

    def item_title(self, item):
        return item.listing_title or item.title

    def item_link(self, item):
        return item.get_full_url(self.request)

    def item_description(self, item):
        return item.listing_summary or item.plain_introduction or item.search_description

    def item_pubdate(self, item):
        return item.publication_date or item.first_published_at

    def item_guid(self, item):
        return item.get_full_url(self.request)

    def item_author_name(self, item):
        if item.author:
            return item.author.title

    def item_categories(self, item):
        if item.topic:
            return [item.topic.title]
        return []
