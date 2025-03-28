from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
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
    renderer_classes = [JSONRenderer]
    #permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PublisherCreateUpdateSerializer
        return PublisherSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    renderer_classes = [JSONRenderer]
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    renderer_classes = [JSONRenderer]
    #permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AuthorCreateUpdateSerializer
        return AuthorSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Autor został pomyślnie dodany.",
            "data": response.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "Autor został zaktualizowany.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "message": "Wybrane pola autora zostały zaktualizowane.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Autor '{instance.first_name} {instance.last_name}' został usunięty."},
            status=status.HTTP_200_OK
        )


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    renderer_classes = [JSONRenderer]
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        'publication_year',
        'category',
        'authors',
        'publisher']
    ordering_fields = ['publication_year', 'title']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BookCreateUpdateSerializer
        return BookSerializer

    # Nowa książka
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Książka została pomyślnie dodana.",
            "data": response.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "Książka została zaktualizowana.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "message": "Wybrane pola książki zostały zaktualizowane.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Książka '{instance.title}' została usunięta."},
            status=status.HTTP_200_OK
        )

class BookDetailsViewSet(viewsets.ModelViewSet):
    queryset = BookDetails.objects.all()
    renderer_classes = [JSONRenderer]
    #permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BookDetailsCreateUpdateSerializer
        return BookDetailsSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Szczegóły książki zostały pomyślnie dodane.",
            "data": response.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "Szczegóły książki zostały zaktualizowane.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "message": "Wybrane pola szczegółów książki zostały zaktualizowane.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Szczegóły książki '{instance.book.title}' zostały usunięte."},
            status=status.HTTP_200_OK
        )


class PatronViewSet(viewsets.ModelViewSet):
    queryset = Patron.objects.all()
    renderer_classes = [JSONRenderer]
    #permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PatronCreateUpdateSerializer
        return PatronSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Patron został pomyślnie dodany.",
            "data": response.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "Patron został zaktualizowany.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "message": "Wybrane pola patrona zostały zaktualizowane.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Patron '{instance.first_name} {instance.last_name}' został usunięty."},
            status=status.HTTP_200_OK
        )

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    renderer_classes = [JSONRenderer]
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'patron']
    ordering_fields = ['borrow_date', 'due_date']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BorrowCreateUpdateSerializer
        return BorrowSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Wypożyczenie zostało pomyślnie dodane.",
            "data": response.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "Wypożyczenie zostało zaktualizowane.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "message": "Wybrane pola wypożyczenia zostały zaktualizowane.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Wypożyczenie książki '{instance.book.title}' zostało usunięte."},
            status=status.HTTP_200_OK
        )


def home_view(request):
    html = """
    <html>
    <head>
        <title>Start - JWT Login</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            h1 { color: #333; }
            input, button {
                padding: 10px;
                margin: 5px 0;
                font-size: 16px;
                width: 300px;
            }
            .link { margin: 15px 0; }
            .token-box {
                background: #eee;
                padding: 10px;
                margin-top: 15px;
                word-break: break-word;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <h1>Strona startowa aplikacji</h1>

        <div class="link"><a href="/admin/">Panel administracyjny</a></div>
        <div class="link"><a href="/api/">REST API</a></div>
        <div class="link"><a href="/graphql/">GraphQL</a></div>
        <div class="link"><a href="/swagger/">Swagger</a></div>
        <div class="link"><a href="/redoc/">ReDoc</a></div>

        <hr/>
        <h2>Uzyskaj token JWT</h2>
        <form id="login-form">
            <input type="text" id="username" placeholder="Nazwa użytkownika" required /><br/>
            <input type="password" id="password" placeholder="Hasło" required /><br/>
            <button type="submit">Zaloguj się</button>
        </form>

        <div id="result"></div>

        <script>
            const form = document.getElementById('login-form');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;

                const response = await fetch('/api/token/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.ok) {
                    document.getElementById('result').innerHTML = `
                        <p>Token uzyskany:</p>
                        <div class="token-box"><strong>Access:</strong><br/>${data.access}</div>
                        <div class="token-box"><strong>Refresh:</strong><br/>${data.refresh}</div>
                    `;
                } else {
                    document.getElementById('result').innerHTML = `
                        <p style="color: red;">Błąd logowania: ${data.detail || 'Nieprawidłowe dane'}</p>
                    `;
                }
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)
