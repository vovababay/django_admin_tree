from typing import Any, Iterable, Optional

from django import template


register = template.Library()


@register.filter
def filter_objects_by_parent(objects: Iterable, args):
    parent_field, parent_id = args
    result = list(filter(lambda obj: (get_parent_id(obj, parent_field) == parent_id), objects))
    return result


@register.filter
def getattribute(value: Any, arg: str) -> Optional[Any]:
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    return None


@register.filter
def get_parent_id(obj: Any, parent_field: str) -> Optional[int]:
    field = getattribute(obj, parent_field)
    if field:
        return field.id
    return None


@register.filter
def tuple_filter(value, arg):
    return (value, arg)


@register.filter
def get_type(value):
    return type(value)

@register.filter
def to_string(value):
    return str(value)