from django.test import TestCase
from django.test import override_settings

from mynewssite.utils.models import ArticleTopic


class ArticleTopicTests(TestCase):
    # This particular test ensures the necessary packages have been imported as calling the save method calls
    # the slugify package would have failed at first
    def test_article_topic_save_generates_slug(self):
        topic = ArticleTopic(title="Another new topic")
        topic.save()

        self.assertEqual(topic.slug, "another-new-topic")

    def test_slugify_without_suffix(self):
        topic = ArticleTopic()
        self.assertEqual(
            topic.slugify("new topic"),
            "new-topic"
        )

    def test_article_topic_slugify_appends_suffix(self):
        topic = ArticleTopic()

        self.assertEqual(
            topic.slugify("new topic", 1),
            "new-topic_1"
        )

    def test_article_topic_saves_preserves_slug(self):
        topic = ArticleTopic(
            title="test save article",
            slug="custom-test-article"
        )

        topic.save()

        self.assertEqual(topic.slug, "custom-test-article")
