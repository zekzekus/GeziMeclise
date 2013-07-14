from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponse
from django.views.generic import (View, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.core.cache import get_cache
from gezimeclise.profiles.models import GeziUser, Report, Region
from gezimeclise.causes.models import Cause
from gezimeclise.profiles.forms import ProfileUpdateForm, ReportForm
from taggit.models import Tag


class ProfileListView(ListView):
    model = GeziUser
    paginate_by = 15
    template_name = "profile/profile_list.html"

    def get_queryset(self):
        cache = get_cache('default')
        if cache.get('profile_list'):
            qs = cache.get('profile_list')
        else:
            qs = super(ProfileListView, self).get_queryset()
            cache.set('profile_list', qs, 600)

        if self.request.GET.get('f') == 'arkadas':
            qs = GeziUser.get_registered_friends(self.request.user)
        # exclude non facebook users
        qs = qs.exclude(facebook_id__isnull=True)
        if self.request.GET.get('q'):
            # search
            q = self.request.GET.get('q')
            qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
        if self.request.GET.get('tag'):
            # tag filter
            tag = self.request.GET.get("tag")
            qs = qs.filter(tags__name__in=["%s" % tag])
        if self.request.GET.get('r'):
            # region filter
            try:
                region_id = int(self.request.GET.get("r"))
            except ValueError:
                pass
            else:
                qs = qs.filter(region__id=region_id)

        # sorting
        if self.request.GET.get('s') == 'pop':
            qs = qs.annotate(number_of_supporters=Count('supporters'))
            qs = qs.order_by('-number_of_supporters')
        else:
            # default sortingp
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

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['causes'] = Cause.objects.filter(user=kwargs['object'])
        context['supported_causes'] = Cause.objects.filter(supporters__id__exact=kwargs['object'].id)
        return context

    def get_queryset(self):
        cache = get_cache('default')
        if cache.get('user_detail-%s' % self.request.user.username):
            qs = cache.get('user_detail-%s' % self.request.user.username)

        else:
            qs = super(ProfileDetailView, self).get_queryset()
            cache.set('user_detail-%s' % self.request.user.username, qs, 600)
        return qs


class ProfileUpdateView(UpdateView):
    model = GeziUser
    success_url = "/"
    slug_field = "username"
    slug_url_kwarg = "username"
    form_class = ProfileUpdateForm
    template_name = "profile/update_profile.html"

    def get_object(self, queryset=None):
        return self.request.user


class ReportCreateView(CreateView):
    model = Report
    success_url = "/"
    form_class = ReportForm
    template_name = "profile/report.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.reporter = self.request.user
        self.object.reported = GeziUser.objects.get(username=self.request.GET.get('username', None))
        self.object.save()
        return super(ReportCreateView, self).form_valid(form)


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


class ProfileDelete(DeleteView):

    template_name = "profile/delete_profile.html"
    success_url = "/"

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
