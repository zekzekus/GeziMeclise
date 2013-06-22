from django.forms import ModelForm
from gezimeclise.blog.models import Post


class CreatePostForm(ModelForm):

    class Meta:
        model = Post
        exclude = ['publisher', 'date_created', 'date_modified', 'slug']
