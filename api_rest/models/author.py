from django.db import models
import uuid

class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Primary Key será um GUID (UUID)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name