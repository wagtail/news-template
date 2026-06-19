from django.test import TestCase

from project_name.utils.models import AuthorSnippet, ArticleTopic, Statistic


class AuthorSnippetTests(TestCase):
    def test_str_returns_title(self):
        author = AuthorSnippet(title="Jane Doe")
        self.assertEqual(str(author), "Jane Doe")


class ArticleTopicTests(TestCase):
    def test_str_returns_title(self):
        topic = ArticleTopic(title="Technology", slug="technology")
        self.assertEqual(str(topic), "Technology")

    def test_slugify_generates_slug(self):
        topic = ArticleTopic(title="Hello World")
        slug = topic.slugify("Hello World")
        self.assertEqual(slug, "hello-world")

    def test_slugify_with_counter(self):
        topic = ArticleTopic(title="Hello World")
        slug = topic.slugify("Hello World", 2)
        self.assertEqual(slug, "hello-world_2")


class StatisticTests(TestCase):
    def test_str_returns_statistic(self):
        stat = Statistic(statistic="100+", description="Happy users")
        self.assertEqual(str(stat), "100+")
