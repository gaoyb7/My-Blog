from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'text', ]
        widgets = {
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
                'text': forms.Textarea(attrs={'class': 'form-contril'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'email', 'comment', ]
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.TextInput(attrs={'class': "form-control"}),
            'comment': forms.Textarea(attrs={'class': "form-control"}),
        }
