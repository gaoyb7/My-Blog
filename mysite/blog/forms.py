from django import forms
from .models import Post, Comment, Message
from bootstrap_markdown.widgets import MarkdownEditor

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'text', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
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


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['username', 'email', 'message', ]
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.TextInput(attrs={'class': "form-control"}),
            'message': forms.Textarea(attrs={'class': "form-control"}),
        }

class UploadFileForm(forms.Form):
    filename = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50)
    file = forms.FileField()
