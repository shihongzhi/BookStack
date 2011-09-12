from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 100)
    publisher = models.CharField(max_length = 100)
    publish_date = models.DateField()
    pages = models.IntegerField()
    ISBN = models.CharField(max_length = 30, unique = True)
    image_src = models.CharField(max_length = 100)
    user = models.ForeignKey(User)
    upload_date = models.DateField(editable=False)
    description = models.TextField()

    class Meta:
        ordering = ['-upload_date']

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.id:
            self.upload_date = datetime.datetime.today()
        super(Book, self).save()

class Comment(models.Model):
    author = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    pub_date = models.DateField()
    content = models.TextField()

    class Meta:
        ordering = ['pub_date']

    def __unicode__(self):
        return "comment by %s at %s" % (self.author.username, self.pub_date.strftime("%Y/%b/%d").lower())

class Bookmark(models.Model):
    STATUS_CHOICES = (
        (u'W',u'want'),
        (u'I',u'reading'),
        (u'D',u'readed'),
    )
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    date = models.DateField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return "%s bookmarked by %s"(self.book, self.user)
