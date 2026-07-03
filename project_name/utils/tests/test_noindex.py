from django.test import TestCase, override_settings
from wagtail.models import Site

from {{ project_name }}.home.models import HomePage


class NoindexTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        site = Site.objects.get(is_default_site=True)
        site.hostname = "testserver"
        site.save()
        cls.home = HomePage.objects.first()

    def setUp(self):
        self.home.refresh_from_db()

    def test_normal_page_does_not_render_noindex(self):
        with override_settings(SEO_NOINDEX=False):
            resp = self.client.get(self.home.url)

        self.assertEqual(200, resp.status_code)
        self.assertNotContains(resp, '<meta name="robots" content="noindex">')

    def test_page_hidden_from_search_results_renders_noindex(self):
        self.home.appear_in_search_results = False
        self.home.save()

        with override_settings(SEO_NOINDEX=False):
            resp = self.client.get(self.home.url)

        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, '<meta name="robots" content="noindex">')

    def test_global_seo_noindex_renders_noindex(self):
        with override_settings(SEO_NOINDEX=True):
            resp = self.client.get(self.home.url)

        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, '<meta name="robots" content="noindex">')
