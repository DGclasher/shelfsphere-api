from books.models import *
from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_books = models.ManyToManyField(
        Book, default=None, related_name='borrowed_by')

    def __str__(self) -> str:
        return self.user.username