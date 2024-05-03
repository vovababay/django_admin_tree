from django import template


register = template.Library()


@register.simple_tag
def verbose_name_tag(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name


@register.filter
def verbose_name_filter(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name


@register.filter
def filter_objects_by_parent(objects, parent_id):
    result = list(filter(lambda obj: (obj.parent_id == parent_id), objects))
    return result

