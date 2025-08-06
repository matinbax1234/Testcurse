# blog/templatetags/custom_tags.py
from django import template
from blog.models import Post, Like

register = template.Library()

@register.simple_tag
def get_all_posts():
    return Post.objects.all().order_by('-created_at')

@register.simple_tag
def get_liked_posts(user):
    if user.is_authenticated:
        return set(Like.objects.filter(user=user).values_list('post_id', flat=True))
    return set()