from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Book
from ..serializers import BookSerializer, BookCreateUpdateSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    renderer_classes = [JSONRenderer]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'category', 'authors', 'publisher']
    ordering_fields = ['publication_year', 'title']

    def get_queryset(self):
        return Book.objects.annotate(borrow_count=Count('borrows'))

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BookCreateUpdateSerializer
        return BookSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Książka została pomyślnie dodana.", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Książka została zaktualizowana.", "data": response.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({"message": "Wybrane pola książki zostały zaktualizowane.", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Książka '{instance.title}' została usunięta."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='full-info')
    def full_info(self, request, pk=None):
        book = self.get_object()
        details = getattr(book, 'detail', None)  # 1:1 relacja
        authors = book.authors.all()  # N:M relacja

        return Response({
            "title": book.title,
            "publication_year": book.publication_year,
            "category": book.category.name if book.category else None,
            "publisher": book.publisher.name,
            "authors": [author.full_name for author in authors],
            "details": {
                "isbn": details.isbn if details else None,
                "pages": details.pages if details else None,
                "cover_image_url": details.cover_image_url if details else None,
            }
        })

    @action(detail=True, methods=['get'], url_path='authors')
    def list_authors(self, request, pk=None):
        book = self.get_object()
        authors = book.authors.all()  # N:M relacja
        data = [
            {
                "id": author.id,
                "first_name": author.first_name,
                "last_name": author.last_name,
                "e-mail": author.email,
                "nationality": author.nationality,
            }
            for author in authors
        ]
        return Response(data)
