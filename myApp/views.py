from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404, redirect
from accounts.models import Follow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



class IndexView(generic.TemplateView):
    template_name = "myApp/index.html"
    
    

class AddPostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "myApp/add_post.html"
    form_class = PostForm
    success_url = reverse_lazy('myApp:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "myApp/post_list.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_ids'] = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        return context
    
    

class FeedPostListView(LoginRequiredMixin, generic.ListView):
    template_name = "myApp/feed_post_list.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        following_ids = Follow.objects.filter(follower=self.request.user).values_list('user_id', flat=True)
        queryset = Post.objects.filter(author_id__in=following_ids).select_related('author').order_by('-created_at')
        return queryset
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_ids'] = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        return context



@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like_exist = Like.objects.filter(user=request.user, post=post)
    if like_exist:
        like_exist.delete()
    else:
        Like.objects.create(user=request.user, post=post)
    return redirect('myApp:post_list')
        
