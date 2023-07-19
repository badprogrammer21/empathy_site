from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('forum/', views.forum, name="forum"),
    path('diary/', views.diary, name="diary"),
    path('register/', views.register, name="register"),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('profile/id<int:id_user>', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('create_profile/id<int:user_id>', views.create_profile, name="create_profile"),
    #path('<int:page_id>', views.forum, name='page'),
    #path('news/', views.news, name="news"),
    #path('<int:page_id>', views.news, name="page"),
    path('article/', views.articles, name="articles"),
    #path('<int:page_id>', views.articles, name="articles"),
]