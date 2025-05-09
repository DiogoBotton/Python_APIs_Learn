from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import AuthorViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
#router.register(r'books', BookViewSet)

# Aqui é necessário adicionar as URL's da API
urlpatterns = [
    #path('', views.get_users, name='get_all_users'),
    path('', include(router.urls))
]