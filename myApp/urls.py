from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
]