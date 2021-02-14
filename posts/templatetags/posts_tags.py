from django import template
from ..models import Comment

register = template.Library()


@register.simple_tag()
def comments_tag(post):
    return Comment.objects.filter(post=post, comment_level=0).count()
