from collections import namedtuple

from django.contrib import admin

from myapp.models import Category
from django_admin_tree.admin import TreeParentAdminMixin
from django_admin_tree.widgets import GfkLookupWidget


@admin.register(Category)
class CategoryAdmin(TreeParentAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'parent')
    max_tree_depth = 3


    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'name':
    #         ct_model = namedtuple('ct_model', [
    #             'model',
    #             'test'
    #         ])
    #         ct = ct_model('test', 'test')
    #         kwargs['widget'] = GfkLookupWidget(
    #             content_type_field_name=ct,
    #             parent_field=Category._meta.get_field('parent'),
    #             app_label=Category._meta.app_label,
    #             model_name=Category._meta.model_name
    #         )
    #
    #     return super().formfield_for_dbfield(db_field, **kwargs)
