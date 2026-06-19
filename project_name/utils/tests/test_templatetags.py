from django.http import QueryDict
from django.test import TestCase, RequestFactory

from project_name.utils.templatetags.util_tags import (
    format_heading_id,
    get_base_querydict,
    clean_querydict,
)


class FormatHeadingIdTests(TestCase):
    def test_generates_slugified_id(self):
        result = format_heading_id("Hello World", "abcdef1234567890")
        self.assertEqual(result, "hello-world-abcdef12")

    def test_truncates_id_to_8_chars(self):
        result = format_heading_id("Test", "1234567890abcdef")
        self.assertEqual(result, "test-12345678")

    def test_handles_special_characters(self):
        result = format_heading_id("Hello & World!", "abcdef12")
        self.assertEqual(result, "hello-world-abcdef12")


class GetBaseQuerydictTests(TestCase):
    def test_returns_empty_querydict_when_no_request_or_base(self):
        result = get_base_querydict({}, None)
        self.assertIsInstance(result, QueryDict)
        self.assertEqual(len(result), 0)

    def test_copies_request_get_when_base_is_none(self):
        factory = RequestFactory()
        request = factory.get("/?foo=bar")
        context = {"request": request}
        result = get_base_querydict(context, None)
        self.assertEqual(result["foo"], "bar")

    def test_copies_querydict_base(self):
        base = QueryDict("a=1&b=2")
        result = get_base_querydict({}, base)
        self.assertEqual(result["a"], "1")
        self.assertEqual(result["b"], "2")

    def test_string_base(self):
        result = get_base_querydict({}, "x=10&y=20")
        self.assertEqual(result["x"], "10")
        self.assertEqual(result["y"], "20")


class CleanQuerydictTests(TestCase):
    def test_removes_none_values(self):
        qd = QueryDict(mutable=True)
        qd.setlist("key", ["value", None])
        clean_querydict(qd)
        self.assertEqual(qd.getlist("key"), ["value"])

    def test_removes_blank_values_when_flag_set(self):
        qd = QueryDict(mutable=True)
        qd.setlist("key", ["value", ""])
        clean_querydict(qd, remove_blanks=True)
        self.assertEqual(qd.getlist("key"), ["value"])

    def test_removes_utm_params(self):
        qd = QueryDict("utm_source=google&foo=bar", mutable=True)
        clean_querydict(qd, remove_utm=True)
        self.assertNotIn("utm_source", qd)
        self.assertEqual(qd["foo"], "bar")

    def test_keeps_utm_params_when_flag_false(self):
        qd = QueryDict("utm_source=google&foo=bar", mutable=True)
        clean_querydict(qd, remove_utm=False)
        self.assertIn("utm_source", qd)
