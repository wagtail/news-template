from django.test import TestCase, RequestFactory

from {{ project_name }}.news.models import NewsListingPage

class TestNewsListingPage(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.page = NewsListingPage(title="Test News")
        # DEFAULT_PER_PAGE = 8
        # MAXIMUM_PAGE_NUMBER = 3
        self.queryset = list(range(18))

    def test_page_has_non_integer_value(self):
        """Page should have integer value"""
        request = self.factory.get('/test-news/?page=abc')
        paginator, page, object_list, is_paginated = self.page.paginate_queryset(self.queryset, request)
        self.assertEqual(page.number, 1)

    def test_page_number_exceeds_maximum_value(self):
        """Page number should not exceed maximum value"""
        request = self.factory.get('/test-news/?page=4')
        paginator, page, object_list, is_paginated = self.page.paginate_queryset(self.queryset, request)
        self.assertEqual(page.number, 3)