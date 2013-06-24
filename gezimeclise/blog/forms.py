from django import forms
from django.forms import ModelForm
from gezimeclise.blog.models import Post
from markitup.widgets import MarkItUpWidget


class CreatePostForm(ModelForm):

    content = forms.CharField(widget=MarkItUpWidget())

    class Meta:
        model = Post
        fields = ['title', 'is_published']
