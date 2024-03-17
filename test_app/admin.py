from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from test_app.models import Category
from django_admin_tree.admin import TreeParentAdminMixin


@admin.register(Category)
class CategoryAdmin(TreeParentAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'parent') #, 'tree_link')
    max_tree_depth = 30






    # def tree_link(self, obj):
    #     url = reverse('admin:%s_%s_tree' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
    #     print(url)
    #     return mark_safe(f'<a href={url}>LINK</a>')

