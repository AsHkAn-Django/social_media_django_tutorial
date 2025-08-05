from . import views
from django.urls import path


app_name = 'myApp'

urlpatterns = [
    path('posts/', views.PostAPIView.as_view(), name='posts'),
]