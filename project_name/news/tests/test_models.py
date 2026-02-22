from django.test import RequestFactory, TestCase, override_settings

from {{ project_name }}.news.models import NewsListingPage


class PaginateQuerysetTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.page = NewsListingPage()
        self.queryset = list(range(1, 25))  # 24 items

    @override_settings(DEFAULT_PER_PAGE=10)
    def test_paginate_queryset_returns_first_page_by_default(self):
        request = self.factory.get("/")
        paginator, page, object_list, is_paginated = self.page.paginate_queryset(
            self.queryset, request
        )
        self.assertEqual(page.number, 1)
        self.assertTrue(is_paginated)

    @override_settings(DEFAULT_PER_PAGE=10)
    def test_paginate_queryset_not_an_integer_falls_back_to_first_page(self):
        request = self.factory.get("/", {"page": "notanumber"})
        paginator, page, object_list, is_paginated = self.page.paginate_queryset(
            self.queryset, request
        )
        self.assertEqual(page.number, 1)

    @override_settings(DEFAULT_PER_PAGE=10)
    def test_paginate_queryset_out_of_range_falls_back_to_last_page(self):
        request = self.factory.get("/", {"page": "999"})
        paginator, page, object_list, is_paginated = self.page.paginate_queryset(
            self.queryset, request
        )
        self.assertEqual(page.number, paginator.num_pages)
