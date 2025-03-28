from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from ..models import Author
from ..serializers import AuthorSerializer, AuthorCreateUpdateSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    renderer_classes = [JSONRenderer]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AuthorCreateUpdateSerializer
        return AuthorSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Autor został pomyślnie dodany.", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Autor został zaktualizowany.", "data": response.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({"message": "Wybrane pola autora zostały zaktualizowane.", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Autor '{instance.first_name} {instance.last_name}' został usunięty."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='books')
    def list_books(self, request, pk=None):
        author = self.get_object()
        books = author.books.all()  # odwrotna relacja N:M z `related_name='books'`
        data = [
            {
                "id": book.id,
                "title": book.title,
                "publication_year": book.publication_year,
                "publisher": book.publisher.name,
                "category": book.category.name if book.category else None
            }
            for book in books
        ]
        return Response({
            "author": author.full_name,
            "books": data
        })