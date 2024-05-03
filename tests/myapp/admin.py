from collections import namedtuple

from django.contrib import admin

from myapp.models import Category
from django_admin_tree.admin import TreeParentAdminMixin


@admin.register(Category)
class CategoryAdmin(TreeParentAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'parent')
    max_tree_depth = 3
    raw_id_fields = ('parent',)

