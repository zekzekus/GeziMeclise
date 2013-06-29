from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, UpdateView, FormView
from gezimeclise.profiles.models import GeziUser, Report, Region
from gezimeclise.profiles.forms import ProfileUpdateForm, ReportForm
from taggit.models import Tag


class FriendsListView(ListView):

    paginate_by = 15
    template_name = "profile/friends_list.html"

    def get_queryset(self):
        qs = GeziUser.get_registered_friends(self.request.user)
        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
        if self.request.GET.get('tag'):
            tag = self.request.GET.get("tag")
            qs = qs.filter(tags__name__in=["%s" % tag])
        if self.request.GET.get('r'):
            try:
                region_id = int(self.request.GET.get("r"))
            except ValueError:
                pass
            else:
                qs = qs.filter(region__id=region_id)

        if self.request.GET.get('s'):
            sorting = self.request.GET.get('s')
            if sorting == 'pop':
                qs = qs.annotate(number_of_supporters=Count('supporters'))
                qs = qs.order_by('-number_of_supporters')
            elif sorting == "son":
                qs = qs.order_by('-date_joined')
        return qs


class ProfileListView(ListView):
    model = GeziUser
    paginate_by = 15
    template_name = "profile/profile_list.html"

    def get_queryset(self):
        qs = super(ProfileListView, self).get_queryset()
        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
        if self.request.GET.get('tag'):
            tag = self.request.GET.get("tag")
            qs = qs.filter(tags__name__in=["%s" % tag])
        if self.request.GET.get('r'):
            try:
                region_id = int(self.request.GET.get("r"))
            except ValueError:
                pass
            else:
                qs = qs.filter(region__id=region_id)

        if self.request.GET.get('s'):
            sorting = self.request.GET.get('s')
            if sorting == 'pop':
                qs = qs.annotate(number_of_supporters=Count('supporters'))
                qs = qs.order_by('-number_of_supporters')
            elif sorting == "son":
                qs = qs.order_by('-date_joined')
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['regions'] = Region.objects.all()
        context['sorting'] = self.request.GET.get('s')
        return context


class ProfileDetailView(DetailView):
    model = GeziUser
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = "profile/profile_detail.html"


class ProfileUpdateView(UpdateView):
    model = GeziUser
    success_url = "/"
    slug_field = "username"
    slug_url_kwarg = "username"
    form_class = ProfileUpdateForm
    template_name = "profile/update_profile.html"

    def get_object(self, queryset=None):
        return self.request.user


class ReportCreateView(FormView):
    model = Report
    success_url = "/"
    form_class = ReportForm
    template_name = "profile/report.html"

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
