from rest_framework import viewsets, status, filters
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date, timedelta
from ..models import Borrow
from ..serializers import BorrowSerializer, BorrowCreateUpdateSerializer

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    renderer_classes = [JSONRenderer]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'patron']
    ordering_fields = ['borrow_date', 'due_date']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BorrowCreateUpdateSerializer
        return BorrowSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Wypożyczenie zostało pomyślnie dodane.", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Wypożyczenie zostało zaktualizowane.", "data": response.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({"message": "Wybrane pola wypożyczenia zostały zaktualizowane.", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Wypożyczenie książki '{instance.book.title}' zostało usunięte."}, status=status.HTTP_200_OK)

    # Zwraca statystyki wypożyczeń
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        stats = {
            "total_borrows": queryset.count(),
            "active": queryset.filter(status='active').count(),
            "overdue": queryset.filter(status='overdue').count(),
            "returned": queryset.filter(status='returned').count(),
        }

        response = super().list(request, *args, **kwargs)
        response.data = {
            "stats": stats,
            "results": response.data
        }
        return response

    # Zwraca szczegóły wypożyczenia
    @action(detail=True, methods=['post'], url_path='return-book')
    def return_book(self, request, pk=None):
        borrow = self.get_object()
        if borrow.status != 'active':
            return Response({'error': 'Tylko aktywne wypożyczenia mogą zostać oznaczone jako zwrócone.'}, status=status.HTTP_400_BAD_REQUEST)
        borrow.status = 'returned'
        borrow.return_date = date.today()
        borrow.save()
        return Response({'message': 'Książka została zwrócona.'}, status=status.HTTP_200_OK)

    # Przedłuża termin zwrotu książki o 30 dni
    @action(detail=True, methods=['post'], url_path='extend-date')
    def extend_due_date(self, request, pk=None):
        borrow = self.get_object()
        if borrow.status != 'active':
            return Response({'error': 'Tylko aktywne wypożyczenia mogą zostać przedłużone.'}, status=status.HTTP_400_BAD_REQUEST)
        borrow.due_date = borrow.due_date + timedelta(days=30)
        borrow.save()
        return Response({'message': 'Termin zwrotu książki został przedłużony o 30 dni.'}, status=status.HTTP_200_OK)

    # Zwraca statystyki wypożyczeń w każdej z możliwych kategorii statusu
    @action(detail=False, methods=['get'], url_path='status-stats')
    def status_stats(self, request):
        queryset = Borrow.objects.values('status').annotate(count=Count('id'))
        return Response({
            "results": list(queryset)
        })

    # Zwraca ile wypozyczył książek każdy z czytelników
    @action(detail=False, methods=['get'], url_path='patron-stats')
    def patron_stats(self, request):
        queryset = (
            Borrow.objects
            .values('patron_id', 'patron__first_name', 'patron__last_name')
            .annotate(total_borrows=Count('id'))
        )
        return Response({"results": list(queryset)})
