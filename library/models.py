from django.db import models
from django.utils import timezone
from datetime import date, timedelta
from django.core.exceptions import ValidationError

# Wydawca
class Publisher(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

# Kategoria
class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    # Klasa Meta dla ustawień modelu, verbose_name_plural -> nazwa w liczbie mnogiej
    # ordering -> domyślne sortowanie
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

# Autor
class Author(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=False, null=False)

    # full_name -> pełne imię i nazwisko
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


# Książka, relacje: N:M z Autor, 1:N z Kategoria, 1:N z Wydawca
class Book(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField(blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True ,related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return self.title

# Szczegóły książki, relacja 1:1 z Książka
class BookDetails(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='detail')
    isbn = models.CharField(max_length=13, blank=False, null=False, unique=True)
    pages = models.IntegerField(blank=True, null=True)
    cover_image_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Szczegóły książki: {self.book.title}"

# Czytelnik
class Patron(models.Model):
    library_card_number = models.CharField(max_length=6, blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=True, null=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

# Cutom manager, tworzenie niestandardowych zapytań
# - aktywne wypożyczenia
class ActiveBorrowManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = 'active')

# - przeterminowane wypożyczenia
class OverdueBorrowManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='overdue')

# - zwrócone wypożyczenia
class ReturnedBorrowManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='returned')

# - zgubione wypożyczenia
class LostBorrowManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='lost')

# - wypożyczenia według statusu
class StatusBorrowManager(models.Manager):
    def by_status(self, status):
        return self.get_queryset().filter(status=status)

# Wypożyczenie, relacje: 1:1 z Książka, 1:1 z Czytelnik
class Borrow(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('overdue', 'Overdue'),
        ('returned', 'Returned'),
        ('lost', 'Lost'),
    )

    patron = models.ForeignKey('Patron', on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='borrows')
    borrow_date = models.DateField(default=date.today)
    return_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Ustawienie managerów
    objects = models.Manager()
    active_borrows = ActiveBorrowManager()
    overdue_borrows = OverdueBorrowManager()
    returned_borrows = ReturnedBorrowManager()
    lost_borrows = LostBorrowManager()
    status_borrows = StatusBorrowManager()

    # Walidacja danych
    def clean(self):
        if self.status in ['returned', 'lost']:
            if not self.return_date:
                raise ValidationError("Return date is required for returned or lost borrow")
            if self.return_date > timezone.now().date():
                raise ValidationError("Return date cannot be in the future")

    # Zapis wypożyczenia
    def save(self, *args, **kwargs):
        if not self.borrow_date:
            self.borrow_date = date.today()
        if self.status == 'active' and not self.due_date:
            self.due_date = self.borrow_date + timedelta(days=30)
        return super().save(*args, **kwargs)

    # Sprawdzenie, czy wypożyczenie jest przeterminowane
    def is_overdue(self):
        return self.status == 'active' and self.due_date and self.due_date < timezone.now().date()

    def __str__(self):
        return f"{self.patron.full_name} borrows {self.book.title}"


