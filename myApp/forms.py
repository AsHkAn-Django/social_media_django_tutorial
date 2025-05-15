from django import forms
from .models import Post, Comment, Like


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
    

