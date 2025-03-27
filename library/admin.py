from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from .models import Publisher, Category, Author, Book, BookDetails, Patron, Borrow
from .resources import (
    PublisherResource,
    CategoryResource,
    AuthorResource,
    BookResource,
    BookDetailsResource,
    PatronResource,
    BorrowResource,
)

@admin.register(Publisher)
class PublisherAdmin(ImportExportModelAdmin):
    resource_class = PublisherResource
    list_display = ("name", "email", "location")
    search_fields = ("name",)

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Author)
class AuthorAdmin(ImportExportModelAdmin):
    resource_class = AuthorResource
    list_display = ("first_name", "last_name", "email", "nationality")
    search_fields = ("first_name", "last_name", "nationality")

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    list_display = ("title", "publisher", "publication_year", "category")
    search_fields = ("title",)
    list_filter = ("publisher", "category", "publication_year")
    filter_horizontal = ("authors",)

@admin.register(BookDetails)
class BookDetailsAdmin(ImportExportModelAdmin):
    resource_class = BookDetailsResource
    list_display = ("book", "isbn", "pages")
    search_fields = ("isbn",)

@admin.register(Patron)
class PatronAdmin(ImportExportModelAdmin):
    resource_class = PatronResource
    list_display = ("library_card_number", "first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "library_card_number")

@admin.register(Borrow)
class BorrowAdmin(ImportExportModelAdmin):
    resource_class = BorrowResource
    list_display = ("patron", "book", "borrow_date", "due_date", "return_date", "status")
    search_fields = ("patron__first_name", "book__title")
    list_filter = ("status",)
