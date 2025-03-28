from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from ..models import BookDetails
from ..serializers import BookDetailsSerializer, BookDetailsCreateUpdateSerializer

class BookDetailsViewSet(viewsets.ModelViewSet):
    queryset = BookDetails.objects.all()
    renderer_classes = [JSONRenderer]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BookDetailsCreateUpdateSerializer
        return BookDetailsSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Szczegóły książki zostały pomyślnie dodane.", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Szczegóły książki zostały zaktualizowane.", "data": response.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({"message": "Wybrane pola szczegółów książki zostały zaktualizowane.", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Szczegóły książki '{instance.book.title}' zostały usunięte."}, status=status.HTTP_200_OK)