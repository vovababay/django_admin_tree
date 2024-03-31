from django.db import models

from django_admin_tree.models import TreeParentModelMixin


class Category(TreeParentModelMixin, models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,  blank=True, related_name='category_parent',
                               verbose_name="Родительская категория")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class TreeMeta:
        parent_field_name = 'parent'

    def __str__(self):
        return f'{self.name}'

