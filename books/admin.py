from django.contrib import admin
from BookStack.books.models import Book,Comment,Bookmark,Tag

admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Bookmark)
admin.site.register(Tag)

