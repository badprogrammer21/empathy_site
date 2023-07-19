from django.urls import path
from .views import *
import pages
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("posts/<slug>/", posts, name="posts"),
    path('<int:page_id>', pages.views.forum, name='page'),
    path("detail/<slug>/", detail, name="details"),
    path("new_forum", new_forum, name="new_forum"),
    path("new_forum/create_post", login_required(PostCreateView.as_view()), name="create_post"),
    path("search_forum_post", search_forum_post, name="search_forum_post"),
    path("category/<slug>/", category_posts, name="category_posts"),
]