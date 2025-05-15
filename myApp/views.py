from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404, redirect



class IndexView(generic.TemplateView):
    template_name = "myApp/index.html"
    
    

class AddPostCreateView(generic.CreateView):
    model = Post
    template_name = "myApp/add_post.html"
    form_class = PostForm
    success_url = reverse_lazy('myApp:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostListView(generic.ListView):
    model = Post
    template_name = "myApp/post_list.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_ids'] = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        return context
    
    
    

class FeedPostListView(generic.ListView):
    template_name = "myApp/feed_post_list.html"
    context_object_name = "posts"



def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like_exist = Like.objects.filter(user=request.user, post=post)
    if like_exist:
        like_exist.delete()
    else:
        Like.objects.create(user=request.user, post=post)
    return redirect('myApp:post_list')
        
