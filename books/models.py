# books/models.py
from django.db import models
from django.core.validators import MinValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title