from rest_framework import serializers
from .models import Publisher, Category, Author, Book, BookDetails, Patron, Borrow

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'email', 'location']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'email', 'nationality', 'full_name']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True, write_only=True, source='authors')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all(), source='publisher', write_only=True)
    borrow_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'authors', 'author_ids', 'category', 'category_id', 'publisher', 'publisher_id', 'borrow_count']

class BookDetailsSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)
    class Meta:
        model = BookDetails
        fields = ['id', 'book', 'book_id', 'isbn', 'pages', 'cover_image_url']

class PatronSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class Meta:
        model = Patron
        fields = ['id', 'first_name', 'last_name', 'email', 'full_name']

class BorrowSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)
    patron = PatronSerializer(read_only=True)
    patron_id = serializers.PrimaryKeyRelatedField(queryset=Patron.objects.all(), source='patron', write_only=True)
    class Meta:
        model = Borrow
        fields = ['id', 'book', 'book_id', 'patron', 'patron_id', 'borrow_date', 'return_date', 'status']

class PublisherCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'email', 'location']

class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AuthorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'email', 'nationality']

class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # Zakładamy, że przy zapisie przesyłamy identyfikatory: publisher, category, authors
        fields = ['id', 'title', 'publisher', 'publication_year', 'category', 'authors']

class BookDetailsCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetails
        fields = ['id', 'book', 'isbn', 'pages', 'cover_image_url']

class PatronCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patron
        fields = ['id', 'first_name', 'last_name', 'email', 'library_card_number']

class BorrowCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'patron', 'book', 'borrow_date', 'due_date', 'return_date', 'status']
