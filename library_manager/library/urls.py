from django.urls import path
from library.views import (AuthorBookCountView, GenreAvgBookCountView, BooksCheckoutView,
                           BookQueryView, BooksInPublicationDateRange, AuthorBookView,
                           UpdateQuantityOfBooks)

urlpatterns = [
    path("author-book-count", AuthorBookCountView.as_view(), name='author_book_count'),
    path("genre-book-count", GenreAvgBookCountView.as_view(), name='genre_book_count'),
    path("books-checkout-details", BooksCheckoutView.as_view(), name='books_checkout_details'),
    path("book-search", BookQueryView.as_view(), name='book_search'),
    path("book-count-on-publication_date", BooksInPublicationDateRange.as_view(), name='book_count_on_publication-date'),
    path("book-count-for-author", AuthorBookView.as_view(), name='book_count_for_author'),
    path("update-quantity-of-books", UpdateQuantityOfBooks.as_view(), name='update_quantity_of_books'),
]