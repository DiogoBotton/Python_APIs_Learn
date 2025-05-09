from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api_rest.models.book import Book
from api_rest.serializers import BookSerializer

class BookApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, *args, **kwargs):
        '''
        Retorna todos os livros
        '''
        # TODO

