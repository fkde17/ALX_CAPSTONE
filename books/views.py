# books/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['copies_available']
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'author', 'published_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        available = self.request.query_params.get('available')
        if available == 'true':
            queryset = queryset.filter(copies_available__gt=0)
        return queryset