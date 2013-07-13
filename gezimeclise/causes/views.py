from django.db.models import Q
from gezimeclise.profiles.models import GeziUser

from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView, View)
from gezimeclise.causes.models import Cause, Comments
from gezimeclise.causes.forms import CauseUpdateForm
from django.http import HttpResponseRedirect, HttpResponse
from taggit.models import Tag
import json


class UsersComments(ListView):

    model = Comments
    template = "causes/comments_list.html"
    context_object_name = "comments"

    def get_queryset(self):
        return self.model.filter(commenter=self.kwargs.username)


class CausesListView(ListView):
    model = Cause
    template = "causes/causes_list.html"
    context_object_name = "causes"

    def get_queryset(self):
        qs = self.model.objects.filter(is_active=True)
        if self.request.GET.get('tag'):
                # tag filter
                tag = self.request.GET.get("tag")
                qs = qs.filter(tags__name__in=["%s" % tag])

        return qs


class CauseDetailView(DetailView):
    model = Cause
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "causes/cause_detail.html"
    context_object_name = "cause"

    def get_context_data(self, **kwargs):
        context = super(CauseDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(cause=self.object)
        commenters = [i['commenter'] for i in Comments.objects.filter(cause=self.object).values('commenter')]
        context['can_comment'] = False if self.request.user.id in commenters else True
        return context

    def post(self, request, slug):
        cause = self.get_object()
        commenter = request.user
        comment = self.request.POST.get("comment")
        Comments.objects.create(commenter=commenter,
                                cause=cause,
                                comment=comment)
        return HttpResponseRedirect("/")


class CauseCreateView(CreateView):

    model = Cause
    template_name = "causes/cause_create.html"
    form_class = CauseUpdateForm
    success_url = "/"

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CauseCreateView, self).form_valid(form)


class CauseSupportView(View):
        def post(self, request):
            username = request.POST.get('username')
            support = request.POST.get('support')
            slug = request.POST.get('slug')

            try:
                user = GeziUser.objects.get(username=username)
                cause = Cause.objects.get(slug=slug)
            except GeziUser.DoesNotExist and Cause.DoesNotExist:
                return HttpResponse("0")
            if support == '+':
                cause.supporters.add(user)
            elif support == '-':
                cause.supporters.remove(user)
            return HttpResponse(support)


class TagsList(View):

    def get(self, context, **response_kwargs):
        if self.request.is_ajax():
            if self.request.GET.get("query"):
                query = self.request.GET.get("query")
                result = [{'name': i.name, 'id': i.id} for i in Tag.objects.filter(name__icontains=query)]
                return HttpResponse(json.dumps(result), mimetype="application/json")
        else:
            return HttpResponse("huloo")