from django.contrib import admin
from BookStack.books.models import Book,Comment,Bookmark

admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Bookmark)

