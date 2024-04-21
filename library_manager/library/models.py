from django.db import models
from base.models import TimeStampedModel
from django.core.exceptions import ValidationError

class GenreTypes(object):
    Science = 1
    Fantasy = 2
    Romance = 3
    History = 4
    Poetry = 5
    Biography = 6
    Drama = 7
    Travel = 8
    Mystery = 9


class Author(TimeStampedModel):
    name = models.CharField(max_length=100)
    biography = models.ForeignKey("Book", related_name="author_biography", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    GENRE_TYPES_CHOICES = (
        (None, "Seleect the genre type"),
        (GenreTypes.Science, "Science"),
        (GenreTypes.Fantasy, "Fantasy"),
        (GenreTypes.Romance, "Romance"),
        (GenreTypes.History, "History"),
        (GenreTypes.Poetry, "Poetry"),
        (GenreTypes.Biography, "Biography"),
        (GenreTypes.Drama, "Drama"),
        (GenreTypes.Travel, "Travel"),
        (GenreTypes.Mystery, "Mystery"),
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='authors_book', on_delete=models.CASCADE, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    publication_date = models.DateTimeField(null=True, blank=True)
    genre = models.PositiveSmallIntegerField(
        choices=GENRE_TYPES_CHOICES, null=True, blank=True, default=None
    )
    quantity_in_stock = models.PositiveIntegerField(null=True, blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    returned_date = models.DateTimeField(null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            raise ValidationError("Title cannot be None")
        if not self.author:
            raise ValidationError("Author cannot be None")

        super(Book, self).save(*args, **kwargs)

        if self.genre ==GenreTypes.Biography:
            author = Author.objects.get(name=self.author.name)
            author.biography = self
            author.save()
        