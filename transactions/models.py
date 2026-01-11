# transactions/models.py
from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from django.db.models import UniqueConstraint

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'book'], condition=models.Q(return_date__isnull=True), name='unique_active_checkout')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"