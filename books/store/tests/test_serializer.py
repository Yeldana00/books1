from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from django.contrib.auth.models import User

from store.models import Book,UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        # create users to annotate like
        user1 = User.objects.create(username='user1', first_name = 'Yeldana', last_name='Kenges')
        user2 = User.objects.create(username='user2', first_name = 'Tangat', last_name='Kenges')
        user3 = User.objects.create(username='user3', first_name = '1', last_name='2')
        book_1 = Book.objects.create(name='Test book 1', price=25,
                                     author_name='Author 1', owner=user1)
        book_2 = Book.objects.create(name='Test book 2', price=55,
                                     author_name='Author 2')
        # create likes for book_1
        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False,)
        # annotated likes
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        data = BooksSerializer(books, many=True).data
        # without annotated likes
        # data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                # add likes_count to annotate
                # 'likes_count': 3,
                # annotate likes
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'user1',
                'readers': [
                    {
                        'first_name': 'Yeldana',
                        'last_name': 'Kenges'
                    },
                    {
                        'first_name': 'Tangat',
                        'last_name': 'Kenges'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    },
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author_name': 'Author 2',
                # add likes_count to annotate
                # 'likes_count': 2,
                # annotate likes
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'Yeldana',
                        'last_name': 'Kenges'
                    },
                    {
                        'first_name': 'Tangat',
                        'last_name': 'Kenges'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    },
                ]
            },
        ]
        self.assertEqual(expected_data, data)

