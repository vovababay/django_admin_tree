from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,  blank=True, related_name='category_parent',
                               verbose_name="Родительская категория")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'

