from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Follow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from mptt.templatetags.mptt_tags import cache_tree_children
from django.db.models import Prefetch



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
        



class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = "myApp/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # build one QuerySet with ALL comments for this post
        all_comments = Comment.objects.filter(post=post)

        # 1) Grab only top-level comments, sorted by '-like'
        # 2) For each of those, prefetch its .children also sorted by '-like'
        parents = (all_comments.filter(parent=None).order_by('-like')
                   .prefetch_related(Prefetch('children',queryset=all_comments
                                              .order_by('-like'),to_attr='sorted_children')))

        context['form']    = CommentForm()
        context['parents'] = parents
        return context
    
    

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user 
            parent_id = form.cleaned_data.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(pk=parent_id)
            comment.save()
            return redirect('myApp:post_detail', pk = pk)
        
    else:
        form = CommentForm()
    return render(request, 'myApp/post_detail.html', {'post': post, 'form': form})
        

@login_required
def vote(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        vote_type = request.POST.get("vote_type")
        
        if vote_type == 'up':
            comment.like += 1
        elif vote_type == 'down':
            comment.like -= 1
        comment.save()
    return redirect('myApp:post_detail', comment.post.pk)