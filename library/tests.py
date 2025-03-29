# library/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, date

from library.models import (
    Publisher, Category, Author, Book, Patron, Borrow
)


class ModelTests(TestCase):

    # tworzenie wydawcy
    def test_create_publisher(self):
        publisher = Publisher.objects.create(
            name="Helion",
            email="kontakt@helion.pl",
            location="POLAND"
        )
        self.assertEqual(publisher.name, "Helion")
        self.assertEqual(publisher.email, "kontakt@helion.pl")
        self.assertEqual(publisher.location, "POLAND")
        self.assertTrue(publisher.id)

    # tworzenie książki
    def test_create_book_with_authors(self):
        cat = Category.objects.create(name="Sci-Fi")
        pub = Publisher.objects.create(name="Solaris")
        author1 = Author.objects.create(first_name="Frank", last_name="Herbert", nationality="USA", email="frank@example.com")
        author2 = Author.objects.create(first_name="John", last_name="Doe", nationality="USA", email="john@example.com")

        book = Book.objects.create(
            title="Dune",
            publisher=pub,
            publication_year=1965,
            category=cat
        )
        book.authors.add(author1, author2)

        self.assertEqual(book.title, "Dune")
        self.assertEqual(book.publisher.name, "Solaris")
        self.assertEqual(book.publication_year, 1965)
        self.assertEqual(book.category.name, "Sci-Fi")
        self.assertEqual(book.authors.count(), 2)

    # sprawdzanie poprawności daty i czy zwrot jest ustawiony na +30 dni
    def test_create_borrow_active(self):
        pub = Publisher.objects.create(name="PWN")
        author = Author.objects.create(first_name="Adam", last_name="Mickiewicz", nationality="Polish", email="adam@example.com")
        cat = Category.objects.create(name="Poetry")
        book = Book.objects.create(
            title="Pan Tadeusz",
            publisher=pub,
            publication_year=1834,
            category=cat
        )
        book.authors.add(author)

        patron = Patron.objects.create(
            library_card_number="123456",
            first_name="Jan",
            last_name="Kowalski",
            email="jan.kowalski@example.com"
        )

        borrow = Borrow.objects.create(patron=patron, book=book)
        self.assertEqual(borrow.status, 'active')
        expected_due_date = borrow.borrow_date + timedelta(days=30)
        self.assertEqual(borrow.due_date, expected_due_date)

    # sprawdzanie czy zmienia się status na 'returned'
    def test_is_overdue_returns_true(self):
        pub = Publisher.objects.create(name="PWN")
        author = Author.objects.create(first_name="Adam", last_name="Mickiewicz", nationality="Polish",
                                       email="adam@example.com")
        cat = Category.objects.create(name="Poetry")
        book = Book.objects.create(
            title="Pan Tadeusz",
            publisher=pub,
            publication_year=1834,
            category=cat
        )
        book.authors.add(author)

        patron = Patron.objects.create(
            library_card_number="123456",
            first_name="Jan",
            last_name="Kowalski",
            email="jan.kowalski@example.com"
        )

        borrow = Borrow.objects.create(
            patron=patron,
            book=book,
            status='active',
            borrow_date=date.today() - timedelta(days=40),  # 40 dni
            due_date=date.today() - timedelta(days=10),     # spóźnione o 10 dni
        )
        self.assertTrue(borrow.is_overdue())
