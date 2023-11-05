from django.db.models import Count, Case, When
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Book, UserBookRelation
from .serializers import BooksSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
    ).select_related('owner').prefetch_related('readers').order_by('id')
    serializer_class = BooksSerializer
    # second lesson filtering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # OAuth
    permission_classes = [IsAuthenticatedOrReadOnly] # read all without authenticate
    filterset_fields = ['price']
    # add search
    search_fields = ['name', 'author_name']
    # add ordering
    ordering_fields = ['price', 'autor_name']

    # permissions
    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated] # должен быть авторизованным
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    # чисто для удобства
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        return obj


# auth
def auth(request):
    return render(request, 'oauth.html')
