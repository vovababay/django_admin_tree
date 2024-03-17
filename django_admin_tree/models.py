

class TreeParentModelMixin:
    def get_descendants(self, max_depth: int = 1):
        SQL_QUERY = """
                WITH RECURSIVE category_tree AS (
                    SELECT id, name, parent_id, 1 as depth
                    FROM {db_table}
                    WHERE id = {object_id}
                    UNION ALL
                    SELECT c.id, c.name, c.parent_id, ct.depth + 1
                    FROM {db_table} c
                    JOIN category_tree ct ON c.parent_id = ct.id
                    WHERE ct.depth < {max_depth}
                )
                SELECT id, name, parent_id
                FROM category_tree
                ORDER BY id;
            """.format(
            db_table=self._meta.db_table,
            object_id=self.id,
            max_depth=max_depth
        )
        objects = self._meta.model.objects.raw(SQL_QUERY)
        return objects

    def check_cycle(self):
        # TODO: Сделать нормальную проверку цикличности рекурсии
        SQL_QUERY = """
        WITH RECURSIVE cycle_check AS (
            SELECT id, parent_id, ARRAY[id] AS path
            FROM {db_table}
            WHERE id = {object_id}
            UNION ALL
            SELECT c.id, c.parent_id, cc.path || c.id
            FROM {db_table} c
            JOIN cycle_check cc ON c.parent_id = cc.id
            WHERE NOT c.id = ANY(cc.path) -- Проверка наличия цикла
        )
        SELECT *
        FROM cycle_check
        WHERE id = ANY(path) AND array_length(path, 1) > 1;
        """.format(
            db_table=self._meta.db_table,
            object_id=self.id,
        )
        cycled_rows = self._meta.model.objects.raw(SQL_QUERY)
        return cycled_rows