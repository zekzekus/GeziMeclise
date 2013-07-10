from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView)
from gezimeclise.causes.models import Cause, Comments
from gezimeclise.causes.forms import CauseUpdateForm
from django.http import HttpResponseRedirect


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


class CauseDetailView(DetailView):
    model = Cause
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "causes/cause_detail.html"
    context_object_name = "cause"

    def get_context_data(self, **kwargs):
        context = super(CauseDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(cause=self.object)
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
    template_name = "cause/cause_create.html"
    form_class = CauseUpdateForm
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CauseCreateView, self).form_valid(form)
