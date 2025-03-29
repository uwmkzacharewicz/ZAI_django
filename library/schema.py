import graphene
from graphene_django import DjangoObjectType
from django.db.models import Count, Avg, Max, Min, Sum
from library.models import Category
from django.db.models import Count
from graphql import GraphQLError
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
    full_name = graphene.String()

    class Meta:
        model = Author
        filter_fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'nationality': ['exact'],
        }
        interfaces = (graphene.relay.Node,)

    def resolve_full_name(self, info):
        return f"{self.first_name} {self.last_name}"


class PatronType(DjangoObjectType):
    full_name = graphene.String()

    class Meta:
        model = Patron
        filter_fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'email': ['icontains'],
            'library_card_number': ['exact'],
        }
        interfaces = (graphene.relay.Node,)

    def resolve_full_name(self, info):
        return f"{self.first_name} {self.last_name}"


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
            'patron__last_name': ['icontains'],
            'book__title': ['icontains'],
            'borrow_date': ['exact', 'gte', 'lte'],
        }
        interfaces = (graphene.relay.Node,)



# Mutacje
class CreateBook(graphene.Mutation):
    book = graphene.Field(BookType)

    class Arguments:
        title = graphene.String()
        publisher_id = graphene.ID()
        publication_year = graphene.Int()
        category_id = graphene.ID()
        authors_ids = graphene.List(graphene.ID)

    def mutate(self, info, title, publisher_id, publication_year, category_id, authors_ids):
        publisher = Publisher.objects.get(pk=publisher_id)
        category = Category.objects.get(pk=category_id)
        authors = Author.objects.filter(pk__in=authors_ids)

        book = Book.objects.create(
            title=title,
            publisher=publisher,
            publication_year=publication_year,
            category=category)

        book.authors.set(authors)
        return CreateBook(book=book)

class UpdateBook(graphene.Mutation):
    book = graphene.Field(BookType)

    class Arguments:
        book_id = graphene.Int(required=True)
        title = graphene.String(required=False)
        publication_year = graphene.Int(required=False)
        publisher_id = graphene.Int(required=False)
        category_id = graphene.Int(required=False)
        author_ids = graphene.List(graphene.Int, required=False)

    def mutate(self, info, book_id, title=None, publication_year=None,
               publisher_id=None, category_id=None, author_ids=None):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise Exception("Nieznaleziono książki.")

        if title is not None:
            book.title = title
        if publication_year is not None:
            book.publication_year = publication_year
        if publisher_id is not None:
            publisher = Publisher.objects.get(pk=publisher_id)
            book.publisher = publisher
        if category_id is not None:
            book.category = Category.objects.get(pk=category_id)

        book.save()

        # ManyToMany
        if author_ids is not None:
            authors = Author.objects.filter(pk__in=author_ids)
            book.authors.set(authors)

        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        book_id = graphene.Int(required=True)

    def mutate(self, info, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise Exception("Book not found.")
        book.delete()
        return DeleteBook(success=True)

# agregacje
class BookPagesStats(graphene.ObjectType):
    total_pages = graphene.Int()
    average_pages = graphene.Float()
    max_pages = graphene.Int()
    min_pages = graphene.Int()


class BookCount(graphene.ObjectType):
    count = graphene.Int()

class CategoryStatsType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    book_count = graphene.Int()

class BookStatsType(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    publication_year = graphene.Int()
    borrow_count = graphene.Int()

class PublicationYearStats(graphene.ObjectType):
    min_year = graphene.Int()
    max_year = graphene.Int()

class BorrowStatusStat(graphene.ObjectType):
    status = graphene.String()
    count = graphene.Int()



class Query(graphene.ObjectType):
    all_books = DjangoFilterConnectionField(BookType)
    all_authors = DjangoFilterConnectionField(AuthorType)
    all_publishers = DjangoFilterConnectionField(PublisherType)
    all_categories = DjangoFilterConnectionField(CategoryType)
    all_patrons = DjangoFilterConnectionField(PatronType)
    all_borrows = DjangoFilterConnectionField(BorrowType)

    # pobranie pojedynczego obiektu po Node ID
    book = graphene.relay.Node.Field(BookType)
    author = graphene.relay.Node.Field(AuthorType)
    publisher = graphene.relay.Node.Field(PublisherType)
    category = graphene.relay.Node.Field(CategoryType)
    patron = graphene.relay.Node.Field(PatronType)
    borrow = graphene.relay.Node.Field(BorrowType)

    # pobranie liczby książek
    book_count = graphene.Field(BookCount)
    # pobranie statystyk kategorii
    category_stats = graphene.List(CategoryStatsType)
    # pobranie statystyk książek
    book_stats = graphene.List(BookStatsType)
    # pobranie statystyk roku wydania
    publication_year_stats = graphene.Field(PublicationYearStats)
    # pobranie statystyk wypożyczeń
    borrow_status_stats = graphene.List(BorrowStatusStat)

    def resolve_book_count(self, info):
        queryset = Book.objects.all()
        result = queryset.aggregate(count=Count("id"))
        total = result["count"]
        #total = Book.objects.aggregate(count=Count("id"))["count"]
        return BookCount(count=total)

    def resolve_category_stats(self, info):
        # słownik z danymi
        qs = (
            Category.objects
            .annotate(book_count=Count('books'))
            .values('id', 'name', 'book_count')
        )

        # zamieniamy słownik na listę obiektów
        stats_list = []
        for row in qs:
            stats_list.append(
                CategoryStatsType(
                    id=row['id'],
                    name=row['name'],
                    book_count=row['book_count']
                )
            )
        return stats_list


    def resolve_book_stats(self, info):
        # słownik z danymi
        qs = (
            Book.objects
            .annotate(borrow_count=Count('borrows'))
            .values('id', 'title', 'publication_year', 'borrow_count')
        )

        # zamieniamy słownik na listę obiektów
        stats_list = []
        for row in qs:
            stats_list.append(
                BookStatsType(
                    id=row['id'],
                    title=row['title'],
                    publication_year=row['publication_year'],
                    borrow_count=row['borrow_count']
                )
            )
        return stats_list

    book_pages_stats = graphene.Field(BookPagesStats)

    def resolve_book_pages_stats(self, info):
        from library.models import BookDetails
        stats = BookDetails.objects.aggregate(
            total_pages=Sum("pages"),
            average_pages=Avg("pages"),
            max_pages=Max("pages"),
            min_pages=Min("pages")
        )
        return BookPagesStats(
            total_pages=stats["total_pages"],
            average_pages=stats["average_pages"],
            max_pages=stats["max_pages"],
            min_pages=stats["min_pages"]
        )

    def resolve_publication_year_stats(self, info):
        stats = Book.objects.aggregate(
            min_year=Min("publication_year"),
            max_year=Max("publication_year")
        )
        return PublicationYearStats(
            min_year=stats["min_year"],
            max_year=stats["max_year"]
        )

    def resolve_borrow_status_stats(self, info):
        stats = (
            Borrow.objects
            .values("status")  # grupujemy po statusie
            .annotate(count=Count("id"))  # zliczamy
            .order_by("status")
        )

        return [
            BorrowStatusStat(status=row["status"], count=row["count"])
            for row in stats
        ]


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)




