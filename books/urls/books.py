# urls for model Book
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from books.models import Book

book_info = {'queryset':Book.objects.all(),
             paginate_by=20}

urlpatterns = patterns('',
                       url(r'^$',
                           object_list,
                           book_info,
                           name='books_book_list'),
                       url(r'^(?P<object_id>\d+)/$',
                           object_detail,
                           book_info,
                           name='books_book_detail'),
                       )
