from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # to searching
    author_name = models.CharField(max_length=255)
    # permissions
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, related_name='my_books')
    # Like, bookmarks
    readers = models.ManyToManyField(User, through='UserBookRelation',
                                     related_name='books')

    def __str__(self):
        return f'Id {self.id}: {self.name}'


class UserBookRelation(models.Model):  # like, rate, bookmark
    RATE_CHOICES = (
        (1, 'OK'),
        (2, 'FINE'),
        (3, 'GOOD'),
        (4, 'AMAZING'),
        (5, 'INCREDIBLE')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # если пользователья удалили зачем нам его лайки его книг
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # если книгу удалили нам неважно кто поставил лайк
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        """
        to admin panel
        :return: id, name
        """
        return f'{self.user.username}: {self.book.name}, RATE: {self.rate}'
