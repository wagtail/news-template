from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from wagtail.models import Page, Site

from project_name.home.models import HomePage
from project_name.news.models import ArticlePage, NewsListingPage
from project_name.utils.models import AuthorSnippet, ArticleTopic


class ArticlePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.home = HomePage.objects.first()
        cls.author = AuthorSnippet.objects.create(title="Test Author")
        cls.topic = ArticleTopic.objects.create(title="Tech", slug="tech")
        cls.news_listing = cls.home.add_child(
            instance=NewsListingPage(title="News", slug="news")
        )
        cls.article = cls.news_listing.add_child(
            instance=ArticlePage(
                title="Test Article",
                slug="test-article",
                author=cls.author,
                topic=cls.topic,
                introduction="Test intro",
            )
        )

    def test_display_date_uses_publication_date(self):
        pub_date = timezone.make_aware(datetime(2025, 3, 15, 12, 0))
        self.article.publication_date = pub_date
        self.assertEqual(self.article.display_date, "15 Mar 2025")

    def test_display_date_falls_back_to_first_published(self):
        self.article.publication_date = None
        self.article.first_published_at = timezone.make_aware(
            datetime(2025, 1, 10, 12, 0)
        )
        self.assertEqual(self.article.display_date, "10 Jan 2025")

    def test_display_date_returns_none_when_no_dates(self):
        self.article.publication_date = None
        self.article.first_published_at = None
        self.assertIsNone(self.article.display_date)

    def test_parent_page_type_is_news_listing(self):
        self.assertEqual(
            ArticlePage.parent_page_types, ["news.NewsListingPage"]
        )


class NewsListingPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.home = HomePage.objects.first()
        cls.news_listing = cls.home.add_child(
            instance=NewsListingPage(title="News", slug="news")
        )

        site = Site.objects.get(is_default_site=True)
        site.hostname = "testserver"
        site.save()

    def test_max_count_is_one(self):
        self.assertEqual(NewsListingPage.max_count, 1)

    def test_subpage_type_is_article(self):
        self.assertEqual(
            NewsListingPage.subpage_types, ["news.ArticlePage"]
        )

    def test_news_listing_page_loads(self):
        response = self.client.get(self.news_listing.url)
        self.assertEqual(response.status_code, 200)

    def test_context_contains_pagination_keys(self):
        response = self.client.get(self.news_listing.url)
        self.assertIn("paginator", response.context)
        self.assertIn("paginator_page", response.context)
        self.assertIn("is_paginated", response.context)
        self.assertIn("topics", response.context)
