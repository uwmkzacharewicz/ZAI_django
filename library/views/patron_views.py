from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from ..models import Patron
from ..serializers import PatronSerializer, PatronCreateUpdateSerializer, BorrowSerializer

class PatronViewSet(viewsets.ModelViewSet):
    queryset = Patron.objects.all()
    renderer_classes = [JSONRenderer]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PatronCreateUpdateSerializer
        return PatronSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Czytelnik został pomyślnie dodany.", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Czytelnik został zaktualizowany.", "data": response.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({"message": "Wybrane pola czytelnika zostały zaktualizowane.", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Czytelnik '{instance.first_name} {instance.last_name}' został usunięty."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='borrows')
    def borrows(self, request, pk=None):
        patron = self.get_object()
        status_param = request.query_params.get('status', None)

        borrows = patron.borrows.all()
        if status_param:
            borrows = borrows.filter(status=status_param)

        serializer = BorrowSerializer(borrows, many=True)
        return Response(serializer.data)
