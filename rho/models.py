from django.db import models

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=50)
    intro = models.CharField(max_length=2000)
    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=50)
    intro = models.CharField(max_length=1500)
    actor = models.ManyToManyField(to="Actor")
    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.CharField(max_length=200)
    movie = models.ForeignKey(Movie ,on_delete = models.CASCADE)
    def __str__(self):
        return self.content

