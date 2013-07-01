from django.forms import ModelForm
from gezimeclise.profiles.models import GeziUser, Report


class ProfileUpdateForm(ModelForm):

    class Meta:
        model = GeziUser
        fields = ['first_name', 'last_name', 'email', 'image',
                  'about_me', 'blog_url', 'causes', 'region', 'tags', 'twitter']


class ReportForm(ModelForm):

    class Meta:
        model = Report
        fields = ['reported', 'topic']
