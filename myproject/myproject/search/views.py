from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page


def search(request):
    search_query = request.GET.get("query")
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "pages/search_view.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "SEO_NOINDEX": bool(
                search_query
            ),  # prevent google from indexing illicit search queries
        },
    )
