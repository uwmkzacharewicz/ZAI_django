from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublisherViewSet,
    CategoryViewSet,
    AuthorViewSet,
    BookViewSet,
    BookDetailsViewSet,
    PatronViewSet,
    BorrowViewSet
)

router = DefaultRouter()
router.register(r'publishers', PublisherViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'bookdetails', BookDetailsViewSet)
router.register(r'patrons', PatronViewSet)
router.register(r'borrows', BorrowViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
