from django.db import models
import uuid

from .author import Author

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Primary Key será um GUID (UUID)
    title = models.CharField(max_length=200)
    published_date = models.DateField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title