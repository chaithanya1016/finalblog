from django.contrib import admin
from django.urls import path,include
from account import views 

urlpatterns = [
    path('signup/',views.signupview, name='signup' ),
    path('login/', views.loginview, name='login'),
    path('loginadmin/', views.loginview, name='loginadmin'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.update_profile, name='updateprofile')

]