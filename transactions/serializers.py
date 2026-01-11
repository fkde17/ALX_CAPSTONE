# transactions/serializers.py
from rest_framework import serializers
from .models import Transaction
from books.serializers import BookSerializer
from users.serializers import UserSerializer

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

class CheckoutSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()