from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, UpdateView,\
    FormView
from gezimeclise.profiles.models import GeziUser, Report
from gezimeclise.profiles.forms import ProfileUpdateForm, ReportForm


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

    def get_object(self, queryset=None):
        return self.request.user


class ReportCreateView(FormView):
    model = Report
    success_url = "/"
    form_class = ReportForm
    template_name="profile/report.html"

    def form_valid(self, form):
        form = form.save(commit=False)
        form.reporter = self.request.user
        form.save()
        return HttpResponse(self.success_url)


class ProfileSupport(View):
    def post(self, request):
        username = self.request.POST.get('username')
        support = self.request.POST.get('support')
        try:
            user = GeziUser.objects.get(username=username)
        except GeziUser.DoesNotExist:
            return HttpResponse("0")
        if not user == request.user:
            if support == '+':
                self.request.user.supports.add(user)
            elif support == '-':
                self.request.user.supports.remove(user)
            return HttpResponse(support)
        else:
            # users cannot support themselves
            return HttpResponse("0")
