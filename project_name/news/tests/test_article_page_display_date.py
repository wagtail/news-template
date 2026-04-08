from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from {{ project_name }}.home.models import HomePage
from {{ project_name }}.news.models import ArticlePage, NewsListingPage
from {{ project_name }}.utils.models import ArticleTopic, AuthorSnippet


class ArticlePageDisplayDateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.home_page = HomePage.objects.first()
        cls.news_listing = cls.home_page.add_child(
            instance=NewsListingPage(title="News", slug="news-display-date-tests")
        )
        cls.news_listing.save_revision().publish()

        cls.author = AuthorSnippet.objects.create(title="Display Date Author")
        cls.topic = ArticleTopic.objects.create(title="Display Date Topic", slug="display-date-topic")

    def _make_article(self, title, slug, publication_date=None, publish=False):
        page = self.news_listing.add_child(
            instance=ArticlePage(
                title=title,
                slug=slug,
                author=self.author,
                topic=self.topic,
                body=[],
                publication_date=publication_date,
            )
        )
        if publish:
            page.save_revision().publish()
            page.refresh_from_db()
        return page

    def test_display_date_uses_publication_date_when_present(self):
        pub_date = timezone.make_aware(datetime(2025, 2, 14, 10, 0, 0))
        article = self._make_article(
            title="Has publication date",
            slug="has-publication-date",
            publication_date=pub_date,
            publish=True,
        )

        self.assertEqual(article.display_date, pub_date.strftime("%d %b %Y"))

    def test_display_date_falls_back_to_first_published_at(self):
        article = self._make_article(
            title="No publication date",
            slug="no-publication-date",
            publication_date=None,
            publish=True,
        )

        self.assertIsNotNone(article.first_published_at)
        self.assertEqual(
            article.display_date,
            article.first_published_at.strftime("%d %b %Y"),
        )

    def test_display_date_is_none_when_unpublished_and_no_publication_date(self):
        article = self._make_article(
            title="Draft without publication date",
            slug="draft-without-publication-date",
            publication_date=None,
            publish=False,
        )

        self.assertIsNone(article.first_published_at)
        self.assertIsNone(article.display_date)