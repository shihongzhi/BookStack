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
