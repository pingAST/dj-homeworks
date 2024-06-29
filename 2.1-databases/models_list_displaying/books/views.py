from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Book
from .converters import DateConverter

date_converter = DateConverter()


def index(request):
    return redirect('book_list')


def book_list(request):
    books = Book.objects.all()

    pub_dates = [book.pub_date for book in books]
    pub_date_format = [date_converter.to_url(date) for date in pub_dates]
    books_with_dates = zip(books, pub_date_format)

    return render(request, 'books/books_list.html', {'books_with_dates': books_with_dates})


def book_list_by_date(request, pub_date):
    pub_date = (date_converter.to_python(pub_date))
    pub_date_txt = date_converter.to_url(pub_date)

    books = Book.objects.filter(pub_date=pub_date)

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    previous_book = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
    next_book = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()

    if previous_book:
        previous_book_date_str = date_converter.to_url(previous_book.pub_date)
    else:
        previous_book_date_str = None

    if next_book:
        next_book_date_str = date_converter.to_url(next_book.pub_date)
    else:
        next_book_date_str = None

    return render(request, 'books/books_list1.html', {
        'books': page_obj,
        'pub_date': pub_date,
        'data_txt': pub_date_txt,
        'previous_book': previous_book,
        'next_book': next_book,
        'previous_book_date_str': previous_book_date_str,
        'next_book_date_str': next_book_date_str,

    })
