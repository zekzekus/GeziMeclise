from django.forms import ModelForm
from gezimeclise.profiles.models import GeziUser


class ProfileUpdateForm(ModelForm):

    class Meta:
        model = GeziUser
        exclude = ['access_token', 'facebook_name', 'facebook_profile_url',
                   'gender', 'facebook_open_graph', 'new_token_required',
                   'supports', 'username', 'is_active', 'date_joined',
                   'is_staff', 'is_superuser', 'groups', 'user_permissions',
                   'password', 'last_login', 'facebook_id', 'raw_data']


