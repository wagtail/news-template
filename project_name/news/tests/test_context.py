from datetime import datetime

from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone

from {{ project_name }}.home.models import HomePage
from {{ project_name }}.news.models import ArticlePage, NewsListingPage
from {{ project_name }}.utils.models import ArticleTopic, AuthorSnippet


class NewsListingGetContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.factory = RequestFactory()

        cls.home = HomePage.objects.first()

        cls.listing = cls.home.add_child(
            instance=NewsListingPage(title="News", slug="news-context-tests")
        )
        cls.listing.save_revision().publish()

        cls.author = AuthorSnippet.objects.create(title="Context Author")

        cls.topic_sports = ArticleTopic.objects.create(title="Sports", slug="sports")
        cls.topic_tech = ArticleTopic.objects.create(title="Tech", slug="tech")
        cls.topic_unused = ArticleTopic.objects.create(title="Unused", slug="unused")

        cls.article_old = cls._make_article(
            title="Old Sports",
            slug="old-sports",
            topic=cls.topic_sports,
            publication_date=timezone.make_aware(datetime(2020, 1, 1, 12, 0, 0)),
        )
        cls.article_new = cls._make_article(
            title="New Tech",
            slug="new-tech",
            topic=cls.topic_tech,
            publication_date=timezone.make_aware(datetime(2024, 1, 1, 12, 0, 0)),
        )

    @classmethod
    def _make_article(cls, title, slug, topic, publication_date):
        page = cls.listing.add_child(
            instance=ArticlePage(
                title=title,
                slug=slug,
                author=cls.author,
                topic=topic,
                body=[],
                publication_date=publication_date,
            )
        )
        page.save_revision().publish()
        page.refresh_from_db()
        return page

    @override_settings(DEFAULT_PER_PAGE=10)
    def test_get_context_without_topic_filter(self):
        request = self.factory.get("/news/")
        context = self.listing.get_context(request)

        self.assertIn("topics", context)
        self.assertIn("matching_topic", context)
        self.assertIn("paginator", context)
        self.assertIn("paginator_page", context)
        self.assertIn("is_paginated", context)

        self.assertFalse(context["matching_topic"])

        topic_slugs = [t["slug"] for t in context["topics"]]
        self.assertIn("sports", topic_slugs)
        self.assertIn("tech", topic_slugs)
        self.assertNotIn("unused", topic_slugs)

        titles = [p.title for p in context["paginator_page"].object_list]
        self.assertEqual(titles[0], "New Tech")
        self.assertEqual(titles[1], "Old Sports")

    @override_settings(DEFAULT_PER_PAGE=10)
    def test_get_context_with_valid_topic_filter(self):
        request = self.factory.get("/news/", {"topic": "sports"})
        context = self.listing.get_context(request)

        self.assertEqual(context["matching_topic"], "sports")
        titles = [p.title for p in context["paginator_page"].object_list]
        self.assertEqual(titles, ["Old Sports"])

    @override_settings(DEFAULT_PER_PAGE=10)
    def test_get_context_with_invalid_topic_filter_is_ignored(self):
        request = self.factory.get("/news/", {"topic": "does-not-exist"})
        context = self.listing.get_context(request)

        self.assertFalse(context["matching_topic"])

        titles = [p.title for p in context["paginator_page"].object_list]
        self.assertIn("New Tech", titles)
        self.assertIn("Old Sports", titles)

    @override_settings(DEFAULT_PER_PAGE=10)
    def test_get_context_with_empty_topic_param_is_ignored(self):
        request = self.factory.get("/news/", {"topic": ""})
        context = self.listing.get_context(request)

        self.assertFalse(context["matching_topic"])
        titles = [p.title for p in context["paginator_page"].object_list]
        self.assertIn("New Tech", titles)
        self.assertIn("Old Sports", titles)