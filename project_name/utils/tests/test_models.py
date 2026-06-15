from django.test import TestCase
from {{ project_name }}.utils.models import ArticleTopic


class ArticleTopicTests(TestCase):
    def test_article_topic_save_generates_slug(self):
        topic = ArticleTopic(title="New topic")
        topic.save()

        self.assertEqual(topic.slug, "new-topic")


    def test_article_topic_save_duplicate_slug_appends_suffix(self):
        topic= ArticleTopic(title="New topic")
        topic.save()

        topic2 = ArticleTopic(title="New topic")
        topic2.save()

        self.assertEqual(topic.slug, "new-topic")
        self.assertEqual(topic2.slug, "new-topic_1")


    def test_article_topic_saves_preserves_slug(self):
        topic = ArticleTopic(
            title="test save article",
            slug="custom-test-article"
        )

        topic.save()

        self.assertEqual(topic.slug, "custom-test-article")
