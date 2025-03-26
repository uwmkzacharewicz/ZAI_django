from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Publisher, Category, Author, Book, BookDetails, Patron, Borrow
from .serializers import (
    PublisherSerializer, PublisherCreateUpdateSerializer,
    CategorySerializer, CategoryCreateUpdateSerializer,
    AuthorSerializer, AuthorCreateUpdateSerializer,
    BookSerializer, BookCreateUpdateSerializer,
    BookDetailsSerializer, BookDetailsCreateUpdateSerializer,
    PatronSerializer, PatronCreateUpdateSerializer,
    BorrowSerializer, BorrowCreateUpdateSerializer
)

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PublisherCreateUpdateSerializer
        return PublisherSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AuthorCreateUpdateSerializer
        return AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'category']
    ordering_fields = ['publication_year', 'title']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BookCreateUpdateSerializer
        return BookSerializer

class BookDetailsViewSet(viewsets.ModelViewSet):
    queryset = BookDetails.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BookDetailsCreateUpdateSerializer
        return BookDetailsSerializer

class PatronViewSet(viewsets.ModelViewSet):
    queryset = Patron.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PatronCreateUpdateSerializer
        return PatronSerializer

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'patron']
    ordering_fields = ['borrow_date', 'due_date']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BorrowCreateUpdateSerializer
        return BorrowSerializer