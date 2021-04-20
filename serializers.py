from rest_framework import serializers
from .models import Book,Profile
from django.contrib.auth.models import User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['author','name','price','lunch_date']

