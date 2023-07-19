from django.urls import path
from article.views import *
import pages

urlpatterns = [
    path('<int:page_id>', pages.views.articles, name='page'),
    path("detail/<slug>/", article_details, name="article_details"),
    path("new_article/", ArticlePostCreateView.as_view(), name="new_article"),
    path("category_detail/<slug>/", category_detail, name="category_detail"),
    path("topic_detail/<slug>/", topic_detail, name="topic_detail"),
    path("article_search/", article_search_post, name="article_search_post"),
]