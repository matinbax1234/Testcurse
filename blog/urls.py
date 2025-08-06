from django.urls import path
from django.views.generic import TemplateView
from blog.models import Post, Like
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', TemplateView.as_view(template_name='blog/home.html'), name='home'),
    path('post/<int:pk>/like/', login_required(lambda request, pk: like_post_view(request, pk)), name='like_post'),
    # سایر URLها
]

def like_post_view(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'liked': liked,
                'total_likes': post.total_likes()
            })
        return redirect('home')
    return redirect('home')