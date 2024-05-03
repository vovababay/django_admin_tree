from django.db import models
from django_admin_tree.models import TreeParentModelMixin

class Category(TreeParentModelMixin, models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,  blank=True, related_name='category_parent',
                               verbose_name="Parent category")
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class TreeMeta:
        parent_field_name = 'parent' # set name field

    def __str__(self):
        return f'{self.name}'