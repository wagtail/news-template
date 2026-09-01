from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks


@hooks.register("insert_global_admin_css")
def insert_onboarding_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("css/admin-onboarding.css"),
    )


@hooks.register("insert_global_admin_js")
def insert_onboarding_js():
    return format_html(
        '<script src="{}"></script>',
        static("js/admin-onboarding.js"),
    )
