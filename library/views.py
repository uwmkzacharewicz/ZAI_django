from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
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
    #permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PublisherCreateUpdateSerializer
        return PublisherSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
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
    #permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AuthorCreateUpdateSerializer
        return AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'category']
    ordering_fields = ['publication_year', 'title']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BookCreateUpdateSerializer
        return BookSerializer

class BookDetailsViewSet(viewsets.ModelViewSet):
    queryset = BookDetails.objects.all()
    #permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BookDetailsCreateUpdateSerializer
        return BookDetailsSerializer

class PatronViewSet(viewsets.ModelViewSet):
    queryset = Patron.objects.all()
    #permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PatronCreateUpdateSerializer
        return PatronSerializer

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'patron']
    ordering_fields = ['borrow_date', 'due_date']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BorrowCreateUpdateSerializer
        return BorrowSerializer

def home_view1(request):
    html = """
    <html>
    <head>
        <title>Strona Główna</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f8f8f8; }
            h1 { color: #333; }
            a { display: block; padding: 10px; background: #4CAF50; color: white; text-decoration: none; margin: 10px 0; width: fit-content; border-radius: 4px; }
            a:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <h1>📚 Witaj w aplikacji biblioteki!</h1>
        <a href="/admin/">Panel administracyjny</a>
        <a href="/api/">REST API</a>
        <a href="/graphql/">GraphQL Playground</a>
        <a href="/swagger/">Swagger UI</a>
        <a href="/redoc/">ReDoc Dokumentacja</a>
    </body>
    </html>
    """
    return HttpResponse(html)

from django.http import HttpResponse

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
        <h1>📚 Strona startowa aplikacji</h1>

        <div class="link"><a href="/admin/">Panel administracyjny</a></div>
        <div class="link"><a href="/api/">REST API</a></div>
        <div class="link"><a href="/graphql/">GraphQL</a></div>
        <div class="link"><a href="/swagger/">Swagger</a></div>
        <div class="link"><a href="/redoc/">ReDoc</a></div>

        <hr/>
        <h2>🔐 Uzyskaj token JWT</h2>
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
                        <p>✅ Token uzyskany:</p>
                        <div class="token-box"><strong>Access:</strong><br/>${data.access}</div>
                        <div class="token-box"><strong>Refresh:</strong><br/>${data.refresh}</div>
                    `;
                } else {
                    document.getElementById('result').innerHTML = `
                        <p style="color: red;">❌ Błąd logowania: ${data.detail || 'Nieprawidłowe dane'}</p>
                    `;
                }
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)
