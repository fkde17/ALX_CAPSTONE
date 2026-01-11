# transactions/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer, CheckoutSerializer
from books.models import Book
from django.utils import timezone
from django.db import transaction

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            try:
                book = Book.objects.select_for_update().get(id=book_id)
                if book.copies_available > 0:
                    # Check if user already has an active checkout for this book
                    if Transaction.objects.filter(user=request.user, book=book, return_date__isnull=True).exists():
                        return Response({'error': 'You already have this book checked out.'}, status=status.HTTP_400_BAD_REQUEST)
                    book.copies_available -= 1
                    book.save()
                    Transaction.objects.create(user=request.user, book=book)
                    return Response({'message': 'Book checked out successfully.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'No copies available.'}, status=status.HTTP_400_BAD_REQUEST)
            except Book.DoesNotExist:
                return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReturnView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        try:
            trans = Transaction.objects.select_for_update().get(id=pk, user=request.user, return_date__isnull=True)
            book = trans.book
            book.copies_available += 1
            book.save()
            trans.return_date = timezone.now()
            trans.save()
            return Response({'message': 'Book returned successfully.'})
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found or already returned.'}, status=status.HTTP_404_NOT_FOUND)