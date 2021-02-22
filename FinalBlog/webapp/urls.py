from django.contrib import admin
from django.urls import path,include
from webapp import views

urlpatterns = [
    path('addpost/', views.addpost_view, name='addpost'),
    path('updatepost/<int:id>/', views.updatepost_view, name='updatepost'),
    path('deletearticle/<int:id>/', views.deletepost_view, name='deletearticle'),

    path('', views.article_list, name='article_list'),
    path('tag/<slug:tag_slug>',views.article_list, name='article_list_by_tag_name'),
    path('<slug:article>/', views.article_details, name='article_details'),
    path('sea', views.SearchResultsView.as_view(), name='search_result'),
    path('search', views.searchposts, name='searchposts'),



]