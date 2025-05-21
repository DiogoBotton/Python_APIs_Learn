from sqlalchemy.orm import Query

class SoftDeleteQuery(Query):
    def not_deleted(self):
        entity = self.column_descriptions[0]['entity']
        if not hasattr(entity, 'deleted_at'):
            raise AttributeError(f"{entity} não possui o atributo 'deleted_at'")
        
        return self.filter(entity.deleted_at.is_(None))