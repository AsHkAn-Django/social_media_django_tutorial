from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('users/<int:pk>/follow_user', views.follow_user.as_view(), name='follow_user'),
    path('users/<int:pk>/update', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('users/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('signup/', views.SignUpCreateView.as_view(), name='signup'),
    path('users/', views.UsersListView.as_view(), name='users'),

]