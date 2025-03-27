from import_export import resources
from .models import Publisher, Category, Author, Book, BookDetails, Patron, Borrow

class PublisherResource(resources.ModelResource):
    class Meta:
        model = Publisher

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        fields = ('id', 'title', 'publisher', 'publication_year', 'category', 'authors')
        export_order = ('id', 'title', 'publisher', 'publication_year', 'category', 'authors')

class BookDetailsResource(resources.ModelResource):
    class Meta:
        model = BookDetails

class PatronResource(resources.ModelResource):
    class Meta:
        model = Patron

class BorrowResource(resources.ModelResource):
    class Meta:
        model = Borrow
