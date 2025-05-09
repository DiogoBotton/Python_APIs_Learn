from django.db import models
import uuid

# Django usa como convenção padrão Snake Case, iremos manter isso na criação das models
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Primary Key será um GUID (UUID)
    name = models.CharField(max_length=150, default='')
    email = models.EmailField(default='', unique=True)
    age = models.IntegerField(default=0)

    # Função "Mágica" para printar a classe
    def __str__(self):
        return f'id: {self.id} | email: {self.email}'