from django import forms
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    text = models.TextField()

    tags = models.ManyToManyField(Tag)
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    visited = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_tag_list(self):
        return [x.tag_name for x in self.tags.all()]

    class Meta:
        ordering = ['-create_date']


class Comment(models.Model):
    post = models.ForeignKey(Post)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    comment = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
    has_read = models.BooleanField(default=False)

    def __str__(self):
        return self.post.title + ' (' + self.username + ')'

    def submit(self):
        self.date_time = timezone.now()
        self.save()

    class Meta:
        ordering = ['-date_time']
