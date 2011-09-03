from django.contrib import admin
from mysite.books.models import Book,Comment

admin.site.register(Book)
admin.site.register(Comment)
