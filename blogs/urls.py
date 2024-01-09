# urls.py

from django.urls import path
from .views import blog_list, add_post, view_post, delete_post, home , about,  SearchView, contactus, SubscribeView

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
     path('contact/', contactus, name='contact'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/add/', add_post, name='add_post'),
    path('blog/<int:post_id>/', view_post, name='view_post'),
    path('blog/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('search/', SearchView.as_view(), name='search_view'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]