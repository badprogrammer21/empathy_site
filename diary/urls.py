from django.urls import path
import pages
from .views import *

urlpatterns = [
    #path('<int:page_id>', pages.views.articles, name='page'),
    path("detail/<slug>/", diary_details, name="diary_details"),
    path("new_diary/", DiaryPostCreateView.as_view(), name="create_diary_post"),
    #path("category_detail/<slug>/", category_detail, name="category_detail"),
    #path("topic_detail/<slug>/", topic_detail, name="topic_detail"),
    #path("article_search/", article_search_post, name="article_search_post"),
]