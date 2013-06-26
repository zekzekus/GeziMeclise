from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, UpdateView,\
    FormView
from gezimeclise.profiles.models import GeziUser, Report
from gezimeclise.profiles.forms import ProfileUpdateForm, ReportForm


class FriendsListView(ListView):
    model = GeziUser
    paginate_by = 15
    template_name="profile/friends_list.html"

    def get_queryset(self):
        return self.model.get_friends(self.request.user)


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
        if self.request.GET.get('c'):
            region = self.request.GET.get("r")
            qs = qs.filter(region__name__icontains=region)
        else:
            return qs

def discover(request, tag_slug=None, loc_slug=None, tag_or_loc_slug=None):
    """
    Parameters to filter content are:
        domain_user: comes from the subdomain, attached to the request object by relevant middleware
        tag or location: if there is one slug, it can be either a location or a tag
        tag and location: if there are two slugs, one is the location and the other is the tag
        
    Query string parameters for filtering and sorting:
        list_type (l): all, own, like (if domain user exists)
        sorting (s): last / popular
        query (q): search query string
    """
    
    # tag / location match
    # we may have both tag and loc slugs or just one tag_or_loc slug
    location = None
    tag = None
    if tag_slug and loc_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        location = get_object_or_404(Location, slug=loc_slug)
    if tag_or_loc_slug:
        try:
            location = Location.objects.get(slug=tag_or_loc_slug)
        except Location.DoesNotExist:
            try:
                tag = Tag.objects.get(slug=tag_or_loc_slug)
            except Tag.DoesNotExist:
                raise Http404

    sorting = request.GET.get('s')
    list_type = request.GET.get('l')
    query = request.GET.get('q')
    
    posts = Post.objects.discover(user=request.domain_user, tag=tag, location=location,
                                  list_type=list_type, query=query)
    
    last_time = None
    if posts.count() > 0:
        last_time = posts[0].time

    if sorting == 'pop':
        posts = posts.order_by('-featured', '-rank')
    
    post_count = posts.count()
    
    context = {'tag': tag,
               'location': location,
               'list_type': list_type,
               'sorting': sorting,
               'last_time': last_time,
               'post_count': post_count}
    
    if not request.is_ajax():
        # skip this part for ajax requests by the infinite scroll
        
        # tags of the posts listed
        tags = Tag.objects.none()
        for post in posts[:60]:
            tags |= post.tags.all()
        tags = tags.distinct()
        
        # locations of the posts listed
        loc_ids = set(posts.values_list('location', flat=True))
        locations = Location.objects.filter(id__in=loc_ids)

        context.update({'tags': tags, 'locations': locations})

    paginator = Paginator(posts, 15)
    page = request.GET.get('p', 1)
    try:
        posts = paginator.page(page)
    except:
        # deliver the first page if page is invalid
        posts = Post.objects.none()
    
    context.update({'posts': posts})

    return render_to_response('usercontent/discover.html', context, 
                              context_instance=RequestContext(request))



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
