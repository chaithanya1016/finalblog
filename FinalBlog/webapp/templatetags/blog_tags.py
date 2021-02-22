from django import template
register = template.Library()
from webapp.models import Article
from django.db.models import Count


@register.simple_tag(name='total_post')
def total_posts():
    return Article.objects.count()

@register.inclusion_tag('webapp/latest_articles.html')
def show_latest_articles():
    latest_posts = Article.objects.order_by('-publish')
    return {'latest_posts': latest_posts}

@register.simple_tag()
def get_most_commented_posts(count=5):
    return Article.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter
def splitByThree(l):
    return [l[i:i+3] for i in range(0, len(l), 3)]


@register.filter
def doubler(l):
    doubled = []
    for num in l:
        doubled.append(num*2)
    return doubled