from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Primary Key será um GUID (UUID)
    Name = models.EmailField(default='', unique=True)
    Email = models.CharField(max_length=150, default='')
    Age = models.IntegerField(default=0)

    # Função "Mágica" para printar a classe
    def __str__(self):
        return f'Id: {self.Id} | E-mail: {self.Email}'