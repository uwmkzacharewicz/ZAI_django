from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Category
from ..serializers import CategorySerializer, CategoryCreateUpdateSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    renderer_classes = [JSONRenderer]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Kategoria została pomyślnie dodana.", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Kategoria została zaktualizowana.", "data": response.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({"message": "Wybrane pola kategorii zostały zaktualizowane.", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Kategoria '{instance.name}' została usunięta."}, status=status.HTTP_200_OK)