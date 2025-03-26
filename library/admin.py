from django.contrib import admin
from .models import Book, Author, Publisher, Category, Borrow, Patron, BookDetails

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Borrow)
admin.site.register(Patron)
admin.site.register(BookDetails)