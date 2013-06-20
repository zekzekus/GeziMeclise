from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.views import generic
from django.views.generic import ListView, DetailView, UpdateView
from gezimeclise.profiles.models import GeziUser
from gezimeclise.profiles.forms import ProfileUpdateForm


class ProfileListView(ListView):
    model = GeziUser
    paginate_by = 15
    template_name = "profile/profile_list.html"

    def get_queryset(self):

        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            return self.model.objects.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q))
        if self.request.GET.get('tag'):
            tag = self.request.GET.get("tag")
            return self.model.objects.filter(tags__name__in=["%s" % tag])
        else:
            return super(ProfileListView, self).get_queryset()


class ProfileDetailView(DetailView):
    model = GeziUser
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = "profile/profile_detail.html"


class ProfileUpdateView(UpdateView):
    model = GeziUser
    success_url = "/"
    form_class = ProfileUpdateForm
    template_name = "profile/update_profile.html"

    def get_object(self,queryset=None):
        return self.request.user


#TODO: Remove support and disable support button when already supported will be added. Will handled during Front end process
class ProfilePostSupport(generic.View):
    def post(self, request):
        if self.request.method == "POST":
            username = self.request.POST.get('username')
            user = GeziUser.objects.get(username=username)
            self.request.user.supports.add(user)
            return HttpResponse("ok")
        else:
            return HttpResponse("nok")