from wagtail.test.utils import WagtailPageTestCase

from {{ project_name }}.home.models import HomePage
from {{ project_name }}.news.models import NewsListingPage, ArticlePage


class NewsPageCreationRulesTests(WagtailPageTestCase):
    def test_article_page_can_be_created_under_news_listing_page(self):
        self.assertCanCreateAt(NewsListingPage, ArticlePage)

    def test_article_page_cannot_be_created_under_home_page(self):
        self.assertCanNotCreateAt(HomePage, ArticlePage)