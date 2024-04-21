import logging
import calendar
from datetime import datetime

from django.shortcuts import render
from django.db.models import F, Count, Q

from rest_framework.views import APIView

from .models import Book, Author
from base import response

logger = logging.getLogger("appLogs")


class AuthorBookCountView(APIView):

    def get(self, request):
        try:
            data = list(Book.objects.annotate(
                author_name=F('author__name')
                ).values('author_name').annotate(book_count=Count('author_name')))
            return response.Ok(data)
        except Exception as e:
            logger.error(f"[AuthorBookCountView] exception occurred - {str(e)}")
            return response.BadRequest({
                "msg": "unable to get book count."
            })

class BooksCheckoutView(APIView):

    def get(self, request):
        try:
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            if not start_date or not end_date:
                logger.info(f"[BooksCheckoutView] start and end date not provided")
            
            # if start or end date not provided taking it as for current month
            start_date = datetime.now().replace(day=1).date()
            end_date = datetime.now().replace(day=calendar.monthrange(datetime.now().year, datetime.now().month)[1]).date()
            data = Book.objects.filter(checkout_date__gte=start_date, checkout_date__lte=end_date).count()
            return response.Ok({
                "count_of_books": data
            })
        except Exception as e:
            logger.error(f"[BooksCheckoutView] exception occurred - {str(e)}")
            return response.BadRequest({
                "msg": "unable to get books checkout data."
            })
    

class BookQueryView(APIView):

    def get(self, request):
        try:
            title_query = request.data.get('title', '')
            author_query = request.data.get('author', '')
            if not title_query and not author_query:
                logger.info(f"[BookQueryView] title and author not provided.")
                return response.BadRequest({
                    "msg": "Please provide title and author."
                })
            books = list(Book.objects.annotate(author_name=F('author__name')).filter(title__icontains=title_query, author__name__icontains=author_query).values(
                'title', 'author_name', 'isbn', 'publication_date', 'genre', 'quantity_in_stock', 'rating'
            ))
            return response.Ok(books)

        except Exception as e:
            logger.error(f"[BookQueryView] exception occurred - {str(e)}")
            return response.BadRequest({
                "msg": "unable to get books."
            })
    

class BooksInPublicationDateRange(APIView):

    def get(self, request):
        try:
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            if not start_date or not end_date:
                logger.info(f"[BooksInPublicationDateRange] start and end date not provided")
                return response.BadRequest({
                    "msg": "Please provide start_date and end_date."
                })
            else:
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                except Exception as e:
                    logger.error(f"[BooksInPublicationDateRange] exception occurred for start_date and end_date- {str(e)}")
                    return response.BadRequest(
                        "Please provide start date and end date in %Y-%m-%d format."
                    )

            books = list(Book.objects.annotate(author_name=F('author__name')).filter(publication_date__range=[start_date, end_date]).values(
                'title', 'author_name', 'isbn', 'publication_date', 'genre', 'quantity_in_stock', 'rating'
            ))
            return response.Ok(books)

        except Exception as e:
            logger.error(f"[BooksInPublicationDateRange] exception occurred - {str(e)}")
            return response.BadRequest({
                "msg": "unable to get books in given publication date range."
            })
    

class AuthorBookView(APIView):
    '''
        This view gives a author data who have writtem books more than some criteria.
    '''
    def get(self, request):
        try:
            author_book_count_query = request.query_params.get('book_count')
            # if count not provided taking default as 5
            if not author_book_count_query:
                author_book_count_query = 5
            authors = list(Author.objects.annotate(count=Count('authors_book')).filter(count__gt=author_book_count_query).values('name'))
            return response.Ok(authors)

        except Exception as e:
            logger.error(f"[AuthorBookView] exception occurred - {str(e)}")
            return response.BadRequest({
                "msg": "unable to get books."
            })


class UpdateQuantityOfBooks(APIView):

    def get(self, request):
        try:
            order_type = request.data.get('order_type')
            book_name = request.data.get('book_name')
            author_name = request.data.get('author_name')
            if not(order_type or book_name or author_name):
                logger.error(f"[UpdateQuantityOfBooks] order_type, book_name and author_name not provided")
                return response.BadRequest({
                    "msg": "Please provide order_type and book_name and author_name"
                })
            try:
                book = Book.objects.get(title=book_name, author__name=author_name)
                if order_type == 'buy_order':
                    if book.quantity_in_stock == 0:
                        return response.BadRequest({
                            "msg": "requested book is out of stock for now. Stay tuned!!"
                        })
                    book.checkout_date = datetime.now()
                    book.quantity_in_stock -= 1
                elif order_type == 'return_order':
                    if not book.checkout_date:
                        return response.BadRequest({
                            "msg": "unable to return book as no order was placed with this book."
                        })
                    book.is_returned = True
                    book.returned_date = datetime.now()
                    book.quantity_in_stock += 1
                book.save()
                return response.Ok({
                    "title": book.title,
                    "author_name": book.author.name,
                    "isbn": book.isbn,
                    "publication_date": book.publication_date,
                    "genre": book.genre,
                    "rating": book.rating,
                })
            except Book.DoesNotExist:
                logger.info(f"[UpdateQuantityOfBooks] book does not exist with {book_name} and {author_name}")
                return response.BadRequest({
                    "msg": "No book found with given name or author"
                })
        except Exception as e:
            logger.error(f"[UpdateQuantityOfBooks] exception occurred - {str(e)}")
            return response.BadRequest({
                "msg": "unable to process order."
            })


class GenreAvgBookCountView(APIView):

    def get(self, request):
        try:
            data = 0
            book_count = Book.objects.count()
            if book_count != 0:
                genre_count = Book.objects.values('genre').distinct().count()
                if genre_count != 0:
                    data = book_count // genre_count
            return response.Ok({
                "count_of_books": data
            })
        except Exception as e:
            logger.error(f"[GenreAvgBookCountView] exception occurred - {str(e)}")
            return response.BadRequest({
                    "msg": "unable to get avg count across genre."
                })