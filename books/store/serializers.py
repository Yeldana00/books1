from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Book, UserBookRelation


class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BooksSerializer(ModelSerializer):
    # optimization ORM
    # likes_count = serializers.SerializerMethodField()
    # annotated likes
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    # optimize ORM
    owner_name = serializers.CharField(source='owner.username', default="", read_only=True)
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        # fields = '__all__'
        # to annotate
        # fields = ('id', 'name', 'price', 'author_name', 'likes_count', 'annotated_likes', 'rating')
        # optimization ORM
        fields = ('id', 'name', 'price', 'author_name', 'annotated_likes', 'rating', 'owner_name', 'readers')

    # optimization ORM
    # def get_likes_count(self, instance):
    #     # запрос в БД
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
