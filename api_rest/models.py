from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Primary Key será um GUID (UUID)
    Name = models.CharField(max_length=150, default='')
    Email = models.EmailField(default='', unique=True)
    Age = models.IntegerField(default=0)

    # Função "Mágica" para printar a classe
    def __str__(self):
        return f'Id: {self.Id} | E-mail: {self.Email}'
    
class Author(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name
    
class Book(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Primary Key será um GUID (UUID)
    Title = models.CharField(max_length=200)
    PublishedDate = models.DateField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.Title