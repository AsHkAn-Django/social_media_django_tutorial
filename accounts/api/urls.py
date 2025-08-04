from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('users/', views.UserAPIView.as_view(), name='users'),
    path('follows/', views.FollowAPIView.as_view(), name='follows'),
]