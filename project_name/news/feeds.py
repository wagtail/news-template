from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.syndication.views import Feed
from wagtail.models import Site

from {{ project_name }}.news.models import ArticlePage, NewsListingPage


class LatestArticlesFeed(Feed):
    """RSS 2.0 feed for public, published news articles."""

    feed_type = Rss201rev2Feed

    def get_object(self, request):
        self.request = request
        site = Site.find_for_request(request) or Site.objects.filter(
            is_default_site=True
        ).first()
        news_listing = self._get_news_listing(site)
        return {
            "request": request,
            "site": site,
            "news_listing": news_listing,
        }

    def _get_news_listing(self, site):
        queryset = NewsListingPage.objects.live().public()
        if site:
            queryset = queryset.descendant_of(site.root_page, inclusive=True)
        return queryset.first()

    def _site_name(self, obj):
        site = obj.get("site")
        if site and site.site_name:
            return site.site_name
        return "News"

    def title(self, obj):
        news_listing = obj.get("news_listing")
        site_name = self._site_name(obj)
        if news_listing:
            return news_listing.seo_title or news_listing.title or site_name
        return site_name

    def description(self, obj):
        news_listing = obj.get("news_listing")
        if news_listing:
            return (
                news_listing.search_description
                or news_listing.listing_summary
                or news_listing.plain_introduction
                or f"Latest articles from {self._site_name(obj)}"
            )
        return f"Latest articles from {self._site_name(obj)}"

    def link(self, obj):
        request = obj.get("request")
        news_listing = obj.get("news_listing")
        if news_listing:
            return news_listing.get_full_url(request)
        return request.build_absolute_uri(reverse("news_feed"))

    def feed_url(self, obj):
        return obj["request"].build_absolute_uri(reverse("news_feed"))

    def items(self, obj):
        queryset = ArticlePage.objects.live().public()
        site = obj.get("site")
        if site:
            queryset = queryset.descendant_of(site.root_page, inclusive=True)
        return (
            queryset.annotate(date=Coalesce("publication_date", "first_published_at"))
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
