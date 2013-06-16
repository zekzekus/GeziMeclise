from django.views.generic import ListView, DetailView
from gezimeclise.profiles.models import GeziUser


class ProfileListView(ListView):
    model = GeziUser
    paginate_by = 15
    template_name = "profile/profile_list.html"

    def get_queryset(self):
        if self.request.GET.get('tag'):
            tag = self.request.GET.get("tag")
            import ipdb
            ipdb.set_trace()
            return self.model.objects.filter(tags__name__in=["%s" % tag])
        else:
            return super(ProfileListView, self).get_queryset()

class ProfileDetailView(DetailView):
    model = GeziUser
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = "profile/profile_detail.html"
