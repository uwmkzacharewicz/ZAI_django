from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from ..models import Publisher, Book
from ..serializers import PublisherSerializer, PublisherCreateUpdateSerializer, BookSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    renderer_classes = [JSONRenderer]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PublisherCreateUpdateSerializer
        return PublisherSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Wydawca został pomyślnie dodany.", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Wydawca został zaktualizowany.", "data": response.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({"message": "Wybrane pola wydawcy zostały zaktualizowane.", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Wydawca '{instance.name}' został usunięty."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='books')
    def list_books(self, request, pk=None):
        publisher = self.get_object()
        books = Book.objects.filter(publisher=publisher)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
