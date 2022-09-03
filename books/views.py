from django.shortcuts import render, redirect
from books.models import Book
from django.core.paginator import Paginator


def books_index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_on_date(request, pub_date):
    template = 'books/books_on_date.html'
    books = Book.objects.all()
    dates = [book.pub_date.strftime('%Y-%m-%d') for book in books]
    uniq_dates = list(set(dates))
    uniq_dates.sort()
    paginator = Paginator(uniq_dates, 1)
    current_page = uniq_dates.index(pub_date) + 1
    books_current_day = Book.objects.filter(pub_date=pub_date)
    current_date_paginator = paginator.get_page(current_page)
    if current_date_paginator.has_previous():
        previous_page_index = current_date_paginator.previous_page_number()-1
        previous_page = uniq_dates[previous_page_index]
    else:
        previous_page = None
    if current_date_paginator.has_next():
        next_page_index = current_date_paginator.next_page_number()-1
        next_page = uniq_dates[next_page_index]
    else:
        next_page = None
    context = {
        'books': books_current_day,
        'current_date_paginator': current_date_paginator,
        'uniq_dates': uniq_dates,
        'previous_page': previous_page,
        'next_page': next_page
    }
    return render(request, template, context)
    