
from typing import Optional

from django import template
from django.template.defaultfilters import slugify
from django.db.models import Model
from django.http.request import QueryDict

register = template.Library()

MODE_ADD = "__add"
MODE_REMOVE = "__remove"
MODE_TOGGLE = "__toggle"


register = template.Library()


@register.simple_tag
def format_heading_id(text, id) -> str:
    """Generate Unique IDs for page headings"""
    # Get the first 8 characters of the ID
    truncated_id = id[:8]

    # Join slugified text and truncated ID
    formatted_text = f"{slugify(text)}-{truncated_id}"

    return formatted_text


# Table of contents
@register.filter(name="table_of_contents_array")
def table_of_contents_array(streamfield_content):
    h2_blocks = [
        (format_heading_id(block.value, block.id), block.value)
        for block in streamfield_content
        if block.block_type == "h2"
    ]

    return h2_blocks


@register.simple_tag(takes_context=True)
def querystring_modify(
    context, base=None, remove_blanks=False, remove_utm=True, **kwargs
):
    """
    Renders a URL and IRI encoded querystring (e.g. "q=Hello%20World&amp;category=1") that is safe to include in links.
    The querystring for the current request (``request.GET``) is used as a base by default, or an alternative
    ``QueryDict``, ``dict`` or querystring value can be provided as the first argument. The base value can be modified
    by providing any number of additional key/value pairs. ``None`` values are discounted automatically, and blank
    values can be optionally discounted by specifying ``remove_blanks=True``.

    When specifying key/value pairs, any keys that do not already exist in the base value will be added, and those
    that do will have their value replaced. Specifying a value of ``None`` for an existing item will result in it being
    discounted. For example, if the querystring for the current request were "foo=ORIGINALFOOVAL&bar=ORIGINALBARVAL",
    but you wanted to:

    * Change the value of "foo" to "NEWFOOVAL"
    * Remove "bar"
    * Add a new "baz" item with the value `1`

    You could do so using the following:

    ```
    
    
    ```

    The output of the above would be "?foo=NEWFOOVAL&amp;baz=1".

    Values can be strings, booleans, integers or references to other variables in the current context.
    For example, if the tag were being used to generate pagination links, where the page number
    was a variable named ``page_num``, you could reference that value like so:

    ```
    
    
    ```

    You can also specify more than one value for a key by providing an iterable as a value. For example, if the context
    contained a variable ``tag_list``, which was list of 'tag' values (```['tag1', 'tag2', 'tag3']```), you include all
    of those values by referencing the list value. For example:

    ```
    
    
    ```

    The output of the above would be "?tags=tag1&amp;tags=tag2&amp;tags=tag3" (plus whatever other values were in the
    base value).

    And finally, if there are potentially multiple values for a specific parameter,
    and you only want to add or remove a single one, you can add '__add' or '__remove'
    to the variable name in your list of modifier kwargs.

    For example, if the querystring was "tags=tag1&amp;tags=tag2&amp;tags=tag3", and you wanted to remove 'tag2', you
    could do:

    ```
    
    
    ```

    Which would output: "?tags=tag1&amp;tags=tag3"

    Or, if you wanted to add a new 'tagNew' value to that same parameter, you could do:

    ```
    
    
    ```

    Which would output: "?tags=tag1&amp;tags=tag2&amp;tags=tag3&amp;tags=tagNew"

    Similarly, if you're unsure whether the value is present or not, and would like to remove it if it is,
    or add it if it is not, you can also use the '__toggle' option. For example:

    ```
    
    
    ```

    You can add as many modifiers to the same tag as you need to, with any
    combination of modifiers at once. For example, the following is perfectly valid:

    ```
    
    
    ```

    Modifiers always fail gracefully if the value you're trying to add is already
    present, or a value you're trying to remove is not, or the named parameter isn't
    present at all.
    """
    querydict = get_base_querydict(context, base)
    for key, value in kwargs.items():

        if isinstance(value, Model):
            value = str(value.pk)
        elif not hasattr(value, "__iter__"):
            value = str(value)

        if key.endswith(MODE_TOGGLE):
            key = key[: -len(MODE_TOGGLE)]
            values = set(querydict.getlist(key))  # type:ignore reportGeneralTypeIssues
            if value in values:
                values.remove(value)
            else:
                values.add(value)
                querydict.setlist(key, list(values))

        elif key.endswith(MODE_ADD):
            key = key[: -len(MODE_ADD)]
            values = set(querydict.getlist(key))  # type:ignore reportGeneralTypeIssues
            if value not in values:
                values.add(value)
                querydict.setlist(key, list(values))

        elif key.endswith(MODE_REMOVE):
            key = key[: -len(MODE_REMOVE)]
            values = set(querydict.getlist(key))  # type:ignore reportGeneralTypeIssues
            if value in values:
                values.remove(value)
                assert hasattr(querydict, "set_list")
                querydict.setlist(key, list(values))

        elif value is None:
            querydict.pop(key, None)
        else:
            if isinstance(value, (str, bytes)):
                querydict[key] = value
            elif hasattr(value, "__iter__") and hasattr(querydict, "setlist"):
                querydict.setlist(key, list(value))

    clean_querydict(querydict, remove_blanks, remove_utm)

    return f"?{querydict.urlencode()}"


def get_base_querydict(context, base):
    if base is None and "request" in context:
        return context["request"].GET.copy()
    if isinstance(base, QueryDict):
        return base.copy()
    if isinstance(base, dict):
        return QueryDict.fromkeys(base, mutable=True)
    if isinstance(base, str):
        return QueryDict(base, mutable=True)
    # request not present or base value unsupported
    return QueryDict("", mutable=True)


def clean_querydict(querydict, remove_blanks=False, remove_utm=True):
    remove_vals: set[Optional[str]] = {None}

    if remove_blanks:
        remove_vals.add("")

    if remove_utm:
        for key in querydict.keys():
            if key.lower().startswith("utm_"):
                querydict.pop(key)

    for key, values in querydict.lists():
        cleaned_values = [v for v in values if v not in remove_vals]
        if cleaned_values:
            querydict.setlist(key, cleaned_values)
        else:
            del querydict[key]
