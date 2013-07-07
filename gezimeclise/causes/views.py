from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView)
from gezimeclise.causes.models import Cause
from gezimeclise.causes.forms import CauseUpdateForm


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