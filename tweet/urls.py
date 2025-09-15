
from django.urls import path

from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),

#seach url
    path("search/", views.tweet_list, name="search_tweets"),

    path('like/<int:tweet_id>/', views.toggle_like, name='toggle_like'),
    path('comment/<int:tweet_id>/', views.add_comment, name='add_comment'),


]


   


