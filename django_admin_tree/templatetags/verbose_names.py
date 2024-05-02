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


@register.filter
def get_add_parent_element(objects, parent_id):
    for i, k in objects.items():
        print(i, k)
        if i == parent_id:
            return k
    # result = list(filter(lambda obj_id, obj: (obj_id == parent_id), objects.items()))
    # print(result)
    result = ' dsadjhsj'
    return result


