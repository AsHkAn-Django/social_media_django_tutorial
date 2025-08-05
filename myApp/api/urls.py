from . import views
from django.urls import path


app_name = 'myApp'

urlpatterns = [
    path('post/<int:pk>/', views.PostAPIView.as_view(), name='posts'),
    path('posts/', views.PostAPIView.as_view(), name='posts'),
]