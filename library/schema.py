import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from library.models import Book, Author, Publisher, Category, Borrow, Patron

class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher
        filter_fields = {
            'name': ['exact', 'icontains'],
            'location': ['icontains'],
        }
        interfaces = (graphene.relay.Node,)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {
            'name': ['exact', 'icontains'],
        }
        interfaces = (graphene.relay.Node,)


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'nationality': ['exact'],
        }
        interfaces = (graphene.relay.Node,)


class PatronType(DjangoObjectType):
    class Meta:
        model = Patron
        filter_fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'email': ['icontains'],
            'library_card_number': ['exact'],
        }
        interfaces = (graphene.relay.Node,)


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        filter_fields = {
            'title': ['icontains', 'exact'],
            'publication_year': ['exact', 'gte', 'lte'],
            'publisher__name': ['icontains'],
            'category__name': ['icontains'],
            'authors__first_name': ['icontains'],
            'authors__last_name': ['icontains'],
        }
        interfaces = (graphene.relay.Node,)


class BorrowType(DjangoObjectType):
    class Meta:
        model = Borrow
        filter_fields = {
            'status': ['exact'],
            'patron__first_name': ['icontains'],
            'book__title': ['icontains'],
            'borrow_date': ['exact', 'gte', 'lte'],
        }
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    all_books = DjangoFilterConnectionField(BookType)
    all_authors = DjangoFilterConnectionField(AuthorType)
    all_publishers = DjangoFilterConnectionField(PublisherType)
    all_categories = DjangoFilterConnectionField(CategoryType)
    all_patrons = DjangoFilterConnectionField(PatronType)
    all_borrows = DjangoFilterConnectionField(BorrowType)

    # Możliwość pobrania pojedynczego obiektu po Node ID
    book = graphene.relay.Node.Field(BookType)
    author = graphene.relay.Node.Field(AuthorType)
    publisher = graphene.relay.Node.Field(PublisherType)
    category = graphene.relay.Node.Field(CategoryType)
    patron = graphene.relay.Node.Field(PatronType)
    borrow = graphene.relay.Node.Field(BorrowType)


schema = graphene.Schema(query=Query)
