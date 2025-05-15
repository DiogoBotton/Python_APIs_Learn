from sqlalchemy.orm import Query

class SoftDeleteQuery(Query):
    def not_deleted(self):
        return self.filter(self._entity_zero().class_.deleted_at.is_(None))