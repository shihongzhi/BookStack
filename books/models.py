from django.db import models
#from tagging.fields import TagField
from BookStack.books import managers
from django.contrib.auth.models import User
#from django.contrib.tagging.fileds import TagField
import datetime

# Tag
# to find books about similar topic
class Tag(models.Model):
	tag = models.CharField(max_length = 100, unique = True)
	#books = models.ManyToManyField('Book')

	# __str__ 
	def __unicode__(self):
		return self.tag
	
# Book
class Book(models.Model):
	title = models.CharField(max_length = 100)
	author = models.CharField(max_length = 100)
	publisher = models.CharField(max_length = 100)
	publish_date = models.DateField()
	pages = models.IntegerField()
	ISBN = models.CharField(max_length = 30, unique = True)
	image_src = models.CharField(max_length = 100)
	# add 
	description = models.TextField()
#	tags = TagField()
	tags = models.CharField(max_length = 30)
	upload_date = models.DateField(editable=False)
	user = models.ForeignKey(User)
        tags = models.ManyToManyField(Tag)
	# Manager
	objects = managers.BookManager()
	class Meta:
		ordering = ['-upload_date']
	
	def __unicode__(self):
		return self.title
	# save /need add args and kwargs arugument ,if not will get an unexpected keyword argumetn 'force_insert'
	def save(self,*args,**kwargs):
		if not self.id:
			self.upload_date = datetime.datetime.today()
		super(Book, self).save(*args,**kwargs)
	# get the url
	@models.permalink
	def get_absolute_url(self): 
		return ('books_book_detail', {'object_id':self.id})

# Comment
class Comment(models.Model):
    author = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    pub_date = models.DateField()
    content = models.TextField()

    class Meta:
        ordering = ['pub_date']

    def __unicode__(self):
        return "comment by %s at %s" % (self.author.username, self.pub_date.strftime("%Y/%b/%d").lower())

# Bookmark : save books for user
# in this way:
# u = User.objects.get(pk=1)
# bookmarks = u.books_bookmark.all() 

class Bookmark(models.Model):
	user = models.ForeignKey(User, related_name='books_bookmark')
	book = models.ForeignKey(Book)
	date = models.DateField()

	class Meta:
		ordering = ['-date']

	def __unicode__(self):
		return "%s bookmarked by %s" % (self.book, self.user)

#	def save(self,force_insert=False, force_update=False):
#		if not self.id:
#			self.date = datetime.datetime.now()
#		super(Bookmark, self).save(force_insert, force_update)

