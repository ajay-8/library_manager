from django.urls import path
from library.views import (AuthorBookCountView, GenreAvgBookCountView, BooksCheckoutView,
                           BookQueryView, BooksInPublicationDateRange, AuthorBookView,
                           UpdateQuantityOfBooks, BookRatingView, home, book_list,
                           author_detail, author_list, book_detail)

urlpatterns = [
    path("author-book-count", AuthorBookCountView.as_view(), name='author_book_count'),
    path("genre-book-count", GenreAvgBookCountView.as_view(), name='genre_book_count'),
    path("books-checkout-details", BooksCheckoutView.as_view(), name='books_checkout_details'),
    path("book-search", BookQueryView.as_view(), name='book_search'),
    path("book-count-on-publication_date", BooksInPublicationDateRange.as_view(), name='book_count_on_publication-date'),
    path("book-count-for-author", AuthorBookView.as_view(), name='book_count_for_author'),
    path("update-quantity-of-books", UpdateQuantityOfBooks.as_view(), name='update_quantity_of_books'),
    path("book-rating", BookRatingView.as_view(), name='book_rating'),
    path("", home, name='home'),
    path('books/', book_list, name='book_list'),
    path('authors/', author_list, name='author_list'),
    path('books/<int:book_id>/', book_detail, name='book_detail'),
    path('authors/<int:author_id>/', author_detail, name='author_detail'),
]