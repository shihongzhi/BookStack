from django.db import models

# Create your models here.
class Book(models.Model):
	title = models.CharField(max_length = 100)
	author = models.CharField(max_length = 100)
	publisher = models.CharField(max_length = 100)
	publish_date = models.DateField()
	pages = models.IntegerField()
	ISBN = models.CharField(max_length = 30, unique = True)
	image_src = models.CharField(max_length = 100)

	def __unicode__(self):
		return self.title


class Comment(models.Model):
    author = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    pub_date = models.DateField()
    content = models.TextField()

    class Meta:
        ordering = ['pub_date']

    def __unicode__(self):
        return "comment by %s at %s" % (self.author.username, self.pub_date.strftime("%Y/%b/%d").lower())

