import django
import os
from django.conf import settings
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from library.models import Publisher, Category, Author, Book, BookDetails, Patron, Borrow
from datetime import date, timedelta
from django.db import connection
from django.core.files import File

def reset_sqlite_sequence(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")

def run():
    print("Czyszczenie danych z bazy...")

    Borrow.objects.all().delete()
    reset_sqlite_sequence('library_borrow')

    BookDetails.objects.all().delete()
    reset_sqlite_sequence('library_bookdetails')

    Book.objects.all().delete()
    reset_sqlite_sequence('library_book')

    Author.objects.all().delete()
    reset_sqlite_sequence('library_author')

    Category.objects.all().delete()
    reset_sqlite_sequence('library_category')

    Publisher.objects.all().delete()
    reset_sqlite_sequence('library_publisher')

    Patron.objects.all().delete()
    reset_sqlite_sequence('library_patron')

    print("Dodawanie danych do bazy...")
    # wydawcy
    p1 = Publisher.objects.create(name="O'Reilly Media", location="USA")
    p2 = Publisher.objects.create(name="Helion", location="Poland")
    p3 = Publisher.objects.create(name="Packt", location="UK")
    p4 = Publisher.objects.create(name="Springer", location="Germany")
    p5 = Publisher.objects.create(name="Addison-Wesley", location="USA")
    p6 = Publisher.objects.create(name="Manning Publications", location="USA")

    # kategorie
    c1 = Category.objects.create(name="Programowanie")
    c2 = Category.objects.create(name="Algorytmy i struktury danych")
    c3 = Category.objects.create(name="Sztuczna inteligencja i uczenie maszynowe")
    c4 = Category.objects.create(name="Zarządzanie projektami IT")
    c5 = Category.objects.create(name="Języki programowania")

    # Tworzymy autorów
    a1 = Author.objects.create(first_name="Robert", last_name="Martin", email="robert.martin@django.com",
                               nationality="USA")
    a2 = Author.objects.create(first_name="Andrew", last_name="Hunt", email="andrew.hunt@django.com", nationality="USA")
    a3 = Author.objects.create(first_name="David", last_name="Thomas", email="david.thomas@django.com",
                               nationality="USA")
    a4 = Author.objects.create(first_name="Thomas", last_name="Cormen", email="thomas.cormen@django.com",
                               nationality="USA")
    a5 = Author.objects.create(first_name="Ian", last_name="Goodfellow", email="ian.goodfellow@django.com",
                               nationality="USA")
    a6 = Author.objects.create(first_name="Kyle", last_name="Simpson", email="kyle.simpson@django.com",
                               nationality="USA")
    a7 = Author.objects.create(first_name="Jerzy", last_name="Grebosz", email="jerzy.grebosz@django.com",
                               nationality="Poland")
    a8 = Author.objects.create(first_name="Tomasz", last_name="Grebski", email="tomasz.grebski@django.com",
                               nationality="Poland")
    a9 = Author.objects.create(first_name="Marcin", last_name="Szeliga", email="marcin.szeliga@django.com",
                               nationality="Poland")
    a10 = Author.objects.create(first_name="Mariusz", last_name="Szymanski", email="mariusz.szymanski@django.com",
                                nationality="Poland")

    # Tworzymy książki i przypisujemy im autorów, kategorię i wydawcę
    b1 = Book.objects.create(title="Clean Code", publisher=p5, publication_year=2008, category=c1)
    b1.authors.add(a1)

    b2 = Book.objects.create(title="The Pragmatic Programmer", publisher=p5, publication_year=1999, category=c1)
    b2.authors.add(a2, a3)

    b3 = Book.objects.create(title="Introduction to Algorithms", publisher=p4, publication_year=2009, category=c2)
    b3.authors.add(a4)

    b4 = Book.objects.create(title="Deep Learning", publisher=p4, publication_year=2016, category=c3)
    b4.authors.add(a5)

    b5 = Book.objects.create(title="You Don't Know JS", publisher=p3, publication_year=2015, category=c5)
    b5.authors.add(a6)

    b6 = Book.objects.create(title="Symfonia C++ Standard", publisher=p2, publication_year=2005, category=c1)
    b6.authors.add(a7)

    b7 = Book.objects.create(title="Algorytmy i struktury danych", publisher=p2, publication_year=2013, category=c2)
    b7.authors.add(a8)

    b8 = Book.objects.create(title="Sztuczna inteligencja i uczenie maszynowe", publisher=p2, publication_year=2020, category=c3)
    b8.authors.add(a9)

    b9 = Book.objects.create(title="Język SQL. Kurs dla początkujących", publisher=p2, publication_year=2018, category=c5)
    b9.authors.add(a9)

    b10 = Book.objects.create(title="Scrum i nie tylko. Teoria i praktyka w zarządzaniu projektami", publisher=p2, publication_year=2019, category=c4)
    b10.authors.add(a10)

    # Tworzymy szczegóły książki

    cover_path = Path(settings.MEDIA_ROOT, "uploads", "clean.jpg")
    with open(cover_path, "rb") as f:
        BookDetails.objects.create(
            book=b1,
            isbn="9780132350884",
            pages=464,
            cover_image_url="https://example.com/clean.jpg",
            cover_image=File(f, name="clean_code.jpg")
        )

    cover_path = Path(settings.MEDIA_ROOT, "uploads", "pragmatic.jpg")
    with open(cover_path, "rb") as f:
        BookDetails.objects.create(
            book=b2,
            isbn="9780135957059",
            pages=352,
            cover_image_url="https://example.com/pragmatic.jpg",
            cover_image=File(f, name="pragmatic_programmer.jpg")
        )


    BookDetails.objects.create(
        book=b3,
        isbn="9780262033848",
        pages=1312,
        cover_image_url="https://example.com/introduction_to_algorithms.jpg",
        cover_image=''
    )

    cover_path = Path(settings.MEDIA_ROOT, "uploads", "deep.jpg")
    with open(cover_path, "rb") as f:
        BookDetails.objects.create(
                book=b4,
                isbn="9780262035613",
                pages=800,
                cover_image_url="https://example.com/deep_learning.jpg",
                cover_image=File(f, name="deep_learning.jpg")
            )

    BookDetails.objects.create(
        book=b5,
        isbn="9781491904244",
        pages=278,
        cover_image_url="https://example.com/you_dont_know_js.jpg"
    )
    BookDetails.objects.create(book=b6, isbn="9788324620845", pages=700, cover_image_url="https://example.com/symfonia_cpp.jpg")
    BookDetails.objects.create(book=b7, isbn="9788328339224", pages=520, cover_image_url="https://example.com/algorytmy_i_struktury_danych.jpg")
    BookDetails.objects.create(book=b8, isbn="9788328339225", pages=480, cover_image_url="https://example.com/sztuczna_inteligencja.jpg")
    BookDetails.objects.create(book=b9, isbn="9788328342140", pages=320, cover_image_url="https://example.com/sql_kurs_poczatkujacych.jpg")
    BookDetails.objects.create(book=b10, isbn="9788328339218", pages=360, cover_image_url="https://example.com/scrum_teoria_praktyka.jpg")

    # Tworzymy czytelników
    pat1 = Patron.objects.create(library_card_number="LC1001", first_name="Jan", last_name="Kowalski", email="jan.kowalski@example.com")
    pat2 = Patron.objects.create(library_card_number="LC1002", first_name="Anna", last_name="Nowak", email="anna.nowak@example.com")
    pat3 = Patron.objects.create(library_card_number="LC1003", first_name="Piotr", last_name="Wiśniewski", email="piotr.wisniewski@example.com")
    pat4 = Patron.objects.create(library_card_number="LC1004", first_name="Maria", last_name="Dąbrowska", email="maria.dabrowska@example.com")
    pat5 = Patron.objects.create(library_card_number="LC1005", first_name="Tomasz", last_name="Lewandowski", email="tomasz.lewandowski@example.com")
    pat6 = Patron.objects.create(library_card_number="LC1006", first_name="Ewa", last_name="Wójcik", email="ewa.wojcik@example.com")
    pat7 = Patron.objects.create(library_card_number="LC1007", first_name="Krzysztof", last_name="Kamiński", email="krzysztof.kaminski@example.com")
    pat8 = Patron.objects.create(library_card_number="LC1008", first_name="Barbara", last_name="Zielińska", email="barbara.zielinska@example.com")
    pat9 = Patron.objects.create(library_card_number="LC1009", first_name="Andrzej", last_name="Szymański", email="andrzej.szymanski@example.com")
    pat10 = Patron.objects.create(library_card_number="LC1010", first_name="Magdalena", last_name="Woźniak", email="magdalena.wozniak@example.com")

    # Tworzymy wypożyczenia (dla uproszczenia używamy bezpośrednio Book zamiast BookCopy)
    Borrow.objects.create(patron=pat1, book=b1, status='active')
    Borrow.objects.create(patron=pat1, book=b2, status='overdue', due_date=date(2024, 2, 3), return_date=date(2024, 1, 20))
    Borrow.objects.create(patron=pat1, book=b3, status='returned', due_date=date(2024, 1, 19), return_date=date(2024, 1, 18))
    Borrow.objects.create(patron=pat2, book=b4, status='lost')
    Borrow.objects.create(patron=pat3, book=b5, status='active')
    Borrow.objects.create(patron=pat3, book=b6, status='returned', due_date=date(2023, 12, 15), return_date=date(2023, 12, 14))
    Borrow.objects.create(patron=pat4, book=b7, status='overdue')
    Borrow.objects.create(patron=pat5, book=b8, status='returned', due_date=date(2024, 1, 15), return_date=date(2024, 1, 14))
    Borrow.objects.create(patron=pat6, book=b9, status='returned', due_date=date(2024, 2, 19), return_date=date(2024, 2, 18))
    Borrow.objects.create(patron=pat6, book=b10, status='returned', due_date=date(2024, 1, 29), return_date=date(2024, 2, 5))
    Borrow.objects.create(patron=pat7, book=b1, status='lost')
    Borrow.objects.create(patron=pat8, book=b2, status='active')
    Borrow.objects.create(patron=pat8, book=b3, status='active')
    Borrow.objects.create(patron=pat1, book=b10, status='active')
    Borrow.objects.create(patron=pat10, book=b4, status='returned', due_date=date(2023, 10, 15), return_date=date(2023, 10, 20))

    print("Dane zostały dodane do bazy.")

if __name__ == '__main__':
    run()


