from django.db.models import Case, IntegerField, QuerySet, When


def order_by_pk_position(
    queryset: QuerySet,
    pks,
    exclude_non_matches = False,
) -> QuerySet:
    """
    Returns the supplied `queryset` ordered according to the
    PK's position in `pks` (a list or tuple of pk values).

    Use the `exclude_non_matches` option to exclude items with
    a PK value not in `pks`.
    """
    if exclude_non_matches:
        queryset = queryset.filter(pk__in=pks)

    cases = (When(pk=value, then=i) for i, value in enumerate(pks))
    return queryset.annotate(
        pk_pos_order=Case(*cases, default=len(pks), output_field=IntegerField())
    ).order_by("pk_pos_order")
