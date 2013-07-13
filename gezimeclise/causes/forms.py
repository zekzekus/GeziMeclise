from django.forms import ModelForm
from gezimeclise.causes.models import Cause


class CauseUpdateForm(ModelForm):

    class Meta:
        model = Cause
        fields = ['title', 'description', 'region', 'tags']

