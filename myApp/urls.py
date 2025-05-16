from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('posts/add', views.AddPostCreateView.as_view(), name='add_post'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/feed', views.FeedPostListView.as_view(), name='feed_post_list'),
    path('posts/like/<int:pk>/', views.like_post, name='like_post'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

]