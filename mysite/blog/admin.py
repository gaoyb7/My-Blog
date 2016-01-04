from django.contrib import admin
from .models import Post, Tag, Comment, Message
from django import forms
from django.db import models


# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)
