import datetime
from markdown import markdown
from django.utils.translation import ugettext as _
from django.template.defaultfilters import safe, striptags, escape
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django import template
from django.template import resolve_variable
from gezimeclise.utils import get_diff_date

register = template.Library()


class UpdateGetNode(template.Node):
    def __init__(self, type, key, value=None):
        self.type = type
        self.key = key
        if value:
            self.var = template.Variable(value)

    def render(self, context):
        get_dict = resolve_variable('request.GET', context).copy()
        if self.type == 'with':
            get_dict[self.key] = self.var.resolve(context)
        else:
            # drop
            try:
                del(get_dict[self.key])
            except KeyError:
                pass
        try:
            # drop page if it is not given explicitly
            if not self.key == 'p':
                del(get_dict['p'])
        except KeyError:
            pass
        q_string = '?'
        for key in get_dict.keys():
            values = get_dict.getlist(key)
            for value in values:
                q_string += '&%s=%s' % (key, value)
        return q_string


class UpdateGet:
    """
    Syntax: {% update_get with state='pct_submitted' %}
            {% update_get drop state %}
    """
    def __call__(self, parser, token):
        tokens = token.contents.split()
        if len(tokens) != 3:
            raise template.TemplateSyntaxError, "%r tag requires 2 arguments" % tokens[0]
        if tokens[1] not in ('with', 'drop'):
            raise template.TemplateSyntaxError, "Second argument in %r tag must be 'with'" % tokens[0]
        if tokens[1] == 'with':
            try:
                key, value = tokens[2].split('=')
            except:
                raise template.TemplateSyntaxError, "A key=value pair should be given as argument"
            return UpdateGetNode('with', key, value)
        else:
            return UpdateGetNode('drop', tokens[2])

register.tag('update_get', UpdateGet())


@register.filter
def likes(user, obj):
    return user in obj.likes.all()


@register.filter
def follows_user(user, other_user):
    if user.is_authenticated():
        if user.get_profile().followed_users.filter(id=other_user.id).count() > 0:
            return True
    return False


@register.filter
def follows_tag(user, tag):
    if user.is_authenticated():
        if user.get_profile().followed_tags.filter(slug=tag.slug).count() > 0:
            return True
    return False


@register.filter
def follows_location(user, location):
    if user.is_authenticated():
        if user.get_profile().followed_locations.filter(slug=location.slug).count() > 0:
            return True
    return False


@register.filter
def flagged_by(content, user):
    if user.is_authenticated():
        if content.flags.filter(id=user.id).count() == 1:
            return True
    return False


@register.filter
def like_count(obj):
    return obj.likes.count()


@register.filter
def diff_date(date):
    if not date:
        return _("unknown")

    return get_diff_date(date)


@register.filter
def naturalday(value):
    today = datetime.date.today()
    value = datetime.date(value.year, value.month, value.day)
    delta = datetime.timedelta(days=1)
    if value == today:
        return _("today")
    elif value == today + delta:
        return _("tomorrow")
    elif value == today - delta:
        return _("yesterday")
    return _(value.strftime('%A'))


@register.filter
def decorated_int(number):
    try:
        if number > 999:
            if number > 9999:
                s = str(number)[:-3]
            else:
                s = str(number)
                s = "%s.%s" % (s[0], s[1])

            return "%sk" % s
        return number
    except:
        return number


@register.filter
def truncate_text(value, limit=80):
    """
    Strips tags and truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|truncate_text }}
        {{ string|truncate_text:50 }}
    """

    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode
    text = unicode(value)

    # no html tags in truncated text; first apply markdown, then strip tags
    text = markdown(text)
    text = striptags(text)

    # Return the string itself if length is smaller or equal to the limit
    if len(text) <= limit:
        return text

    # Cut the string
    text = text[:limit]

    # Break into words and remove the last
    words = text.split(' ')[:-1]

    # Join the words and return
    text = ' '.join(words) + '...'

    return safe(escape(text))


@register.filter
def render_text(text):
    """
    For full texts
    """
    return safe(markdown(striptags(text)))


@register.filter
def thumb_layout(photos):
    if len(photos) == 0:
        return
    elif len(photos) == 1:
        # 1 yatay 1 dikey
        return mark_safe('''<a href="%(photo_url)s" rel="galeri[%(post_id)s]">%(thumb_large)s</a>''' % {
                                'photo_url': photos[0].image.url,
                                'post_id': photos[0].post.id,
                                'thumb_large': render_to_string('usercontent/thumb_large.html', {'photo': photos[0]})
                                })
    elif len(photos) >= 2:

        big_image_count = 2
        max_thumb_count = 3

        photo_subset = photos[:big_image_count]
        photo_thumbs = photos[len(photo_subset):len(photo_subset) + max_thumb_count]
        other_photos = []
        if len(photo_subset) + len(photo_thumbs) < len(photos):
            # 'we have extra photos'
            other_photos = photos[len(photo_subset) + len(photo_thumbs):]
        portraits = []
        landscapes = []
        for photo in photo_subset:
            if photo.image.width < photo.image.height:
                portraits.append(photo)
            else:
                landscapes.append(photo)

        if len(portraits) == 2 and len(landscapes) == 0:
            span_first = 'span12'
            span_last = 'span12'
            photo_first = portraits[0]
            photo_last = portraits[1]
        elif len(portraits) == 1 and len(landscapes) == 1:
            span_first = 'span8'
            span_last = 'span16'
            photo_first = portraits[0]
            photo_last = landscapes[0]
        elif len(portraits) == 0 and len(landscapes) == 2:
            span_first = 'span12'
            span_last = 'span12'
            photo_first = landscapes[0]
            photo_last = landscapes[1]

        return mark_safe('''%(thumbs_row_layout)s''' %
                        {
                            'thumbs_row_layout': render_to_string('usercontent/thumbs_layout.html',
                                {
                                    'photo_first': photo_first,
                                    'photo_last': photo_last,
                                    'span_first': span_first,
                                    'span_last': span_last,
                                    'photo_thumbs': photo_thumbs,
                                    'other_photos': other_photos
                                })
                        })


@register.filter(is_safe=False)
def merge_string(value, arg):
    '''Merge string.'''
    try:
        return str(value) + str(arg)
    except (TypeError):
        return ''
