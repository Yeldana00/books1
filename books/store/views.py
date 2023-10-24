from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Book
from .serializers import BooksSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    # second lesson filtering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # OAuth
    permission_classes = [IsAuthenticated]
    filterset_fields = ['price']
    # add search
    search_fields = ['name', 'author_name']
    # add ordering
    ordering_fields = ['price', 'autor_name']


# auth
def auth(request):
    return render(request, 'oauth.html')
