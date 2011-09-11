from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum

class BookManager(models.Manager):
    def top_authors(self):
        return User.objects.annotate(score=Count('book')).order_by('-score')

    def most_bookmarked(self):
        return self.annotate(score=Count('bookmark')).order_by('-score')
