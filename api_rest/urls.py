from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .features.authors import AuthorViewSet
from .features.users import get_users

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
#router.register(r'books', BookViewSet)

# Aqui é necessário adicionar as URL's da API
urlpatterns = [
    path('', include(router.urls)),
    path('users/', get_users, name='get_all_users') # Manual
]