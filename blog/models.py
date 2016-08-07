from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author)
    category = models.ManyToManyField(Category,  related_name='catalog')
    image = models.ImageField(upload_to="media/articles/")
    description = models.TextField()
    published_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.title

