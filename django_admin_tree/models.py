from django.core.exceptions import ValidationError
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.utils.translation import gettext as _


class TreeParentModelMixin:
    def __init__(self, *args, **kwargs):
        self.parent_field = getattr(self.__class__, self.TreeMeta.parent_field_name)
        self.parent_field_db_name = self.parent_field.field.get_attname()
        super().__init__(*args, **kwargs)

    def get_descendants(self, max_depth: int = None):
        SQL_QUERY = """
                WITH RECURSIVE tree AS (
                    SELECT id, {parent_field_db_name}, 1 as depth
                    FROM {db_table}
                    WHERE id = {object_id}
                    UNION ALL
                    SELECT c.id, c.{parent_field_db_name}, ct.depth + 1
                    FROM {db_table} c
                    JOIN tree ct ON c.{parent_field_db_name} = ct.id
                    {filter_max_depth}
                )
                SELECT id, {parent_field_db_name}
                FROM tree
                ORDER BY id;
            """.format(
            db_table=self._meta.db_table,
            object_id=self.id,
            parent_field_db_name=self.parent_field_db_name,
            filter_max_depth='WHERE ct.depth < {max_depth}'.format(max_depth=max_depth) if max_depth else ''
        )
        objects = self._meta.model.objects.raw(SQL_QUERY)
        return objects

    def is_cycled(self):
        if not self.id:
            return False
        descendants = [descendant.id for descendant in self.get_descendants()]
        parent_id = getattr(self, self.parent_field_db_name)
        if parent_id in descendants:
            return True
        return False

    def clean(self):
        if self.is_cycled():
            parent_id = getattr(self, self.parent_field_db_name)
            raise ValidationError(message=_('parent {} create recursion').format(parent_id))

    class TreeMeta:
        parent_field_name = 'parent'

