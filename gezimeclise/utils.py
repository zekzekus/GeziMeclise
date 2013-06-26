from urlparse import parse_qs
from unidecode import unidecode
from django.template.defaultfilters import slugify as slgfy
from django.utils.translation import ugettext_lazy as _, ungettext
from datetime import datetime

IGNORED_WORDS = ['cd', 'mh', 'tr']


def slugify(s, max_length=50, max_words=None):
    if s == '':
        return s
    slug = slgfy(unidecode(s))
    # remove ignored words
    slug = '-'.join([w for w in slug.split('-') if w not in IGNORED_WORDS])
    while len(slug) > max_length:
        # try to shorten word by word
        temp = slug[:slug.rfind('-')]
        if len(temp) > 0:
            slug = temp
        else:
            # we have nothing left, do not apply the last crop, apply the cut-off directly
            slug = slug[:max_length]
            break
    if max_words:
        words = slug.split('-')[:max_words]
        slug = '-'.join(words)
    return slug


def get_diff_date(date):
    now = datetime.now()
    diff = now - date
    days = diff.days
    hours = int(diff.seconds / 3600)
    minutes = int(diff.seconds / 60)

    if days > 2:
        if date.year == now.year:
            return _(u'%(month)s %(day)s') % {'month': _(date.strftime('%B')),
                                              'day': date.strftime('%d')}
        else:
            return _(u"%(month)s %(day)s '%(year)s") % {'month': _(date.strftime('%B')),
                                                        'day': date.strftime('%d'),
                                                        'year': date.strftime('%y')}
    elif days == 2:
        return _('2 days ago')
    elif days == 1:
        return _('yesterday')
    elif minutes >= 60:
        return ungettext('%(hr)d hour ago', '%(hr)d hours ago', hours) % {'hr': hours}
    elif diff.seconds >= 60:
        return ungettext('%(min)d min ago', '%(min)d mins ago', minutes) % {'min': minutes}
    else:
        return _('just now')
