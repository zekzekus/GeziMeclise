from django.views.generic import ListView, DetailView
from gezimeclise.profiles.models import GeziUser


class ProfileListView(ListView):
    model = GeziUser
    paginate_by = 15
    template_name = "profile/profile_list.html"


class ProfileDetailView(DetailView):
    model = GeziUser