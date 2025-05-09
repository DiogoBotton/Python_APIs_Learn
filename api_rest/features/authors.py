from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api_rest.models.author import Author
from api_rest.serializers import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] # Liberando todos os endpoints para não necessitar autenticação

    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer