# django-admin-tree


Install [PyPi](https://pypi.org/project/django-admin-tree/) lib

```bash
pip install django-admin-tree
```

### settings.py
```python
INSTALLED_APPS = [
    ...
    'django_admin_tree',
    ...
]
```

### models.py

#### !!! You must specify the parent_field_name value in TreeMeta
```python
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
```


### admin.py
#### !!! You must specify the max_tree_depth value in admin class, otherwise the output will be all
```python
from django.contrib import admin

from test_app.models import Category
from django_admin_tree.admin import TreeParentAdminMixin


@admin.register(Category)
class CategoryAdmin(TreeParentAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'parent')
    max_tree_depth = 3

```
[Example](ONE_FK_README.md)

### set fixtures for test
```python
python manage.py loaddata --format json fixtures/category.json
```
