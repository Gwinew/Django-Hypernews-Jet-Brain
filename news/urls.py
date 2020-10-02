from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.index, name='news'),
    path('news/<int:news_id>/', views.detail, name='detail'),
    path('news/create/', views.create, name='create'),
]
