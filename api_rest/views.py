from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models import User, Author, Book
from .serializers import UserSerializer, BookSerializer, AuthorSerializer

import json

# Exemplos de consultas do banco de dados
# data = User.objects.get(Id='') # Retorna um objeto (GetById)
# data = User.objects.filter(Age=25) # Retorna uma queryset (lista), retorna os que tem 25 anos
# data = User.objects.exclude(Age=25) # Retorna todos os objetos que não tem o paramêtro especificado (retorna os que não tem 25 anos)
# data.save()
# data.delete()

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()

    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)

class AuthorViewSet(viewsets.ModelViewSet): # TODO: Falta resolver problema com autenticação (Como faz a autenticação?)
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer