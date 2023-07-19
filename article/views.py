from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView
from .models import ArticlePost, ArticleCategory, Author
from django.utils.decorators import method_decorator
from django import template
from taggit.models import Tag
from .forms import ArticlePostForm


def article_search_post(request):
    category = ArticleCategory.objects.order_by('title')
    queryset_list = ArticlePost.objects.filter(approved=True)
    all_posts = ArticlePost.objects.all()
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(content__icontains=keywords)
    return render(request, 'articles/search.html', {
        'posts_search': queryset_list,
        'categories': category,
        'all_posts': all_posts,
        "cats": zip(
            category,
            [len(ArticlePost.objects.filter(categories=cat)) for cat in category]
        ),
    })

def category_detail(request, slug):
    category = get_object_or_404(ArticleCategory, slug=slug)
    posts = ArticlePost.objects.filter(approved=True, categories=category)
    category2 = ArticleCategory.objects.order_by('title')

    context = {
        "ct": category,
        "categories": category2,
        "posts": posts,
    }

    return render(request, 'articles/categories.html', context)


def topic_detail(request, slug):
    context = {
        "categories": ArticleCategory.objects.all(),
        "tag_name": slug,
        "posts": list(set([post for post in ArticlePost.objects.filter(approved=True)
                           for tag in post.article_tags.all() 
                           if tag.name == slug])),
    }

    return render(request, 'articles/topics.html', context)


class ArticlePostCreateView(CreateView):
    model = ArticlePost
    template_name = 'articles/new_article.html'
    form_class = ArticlePostForm

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.article_users = Author.objects.get(user=self.request.user)  # use your own profile here
        candidate.save()
        return super(ArticlePostCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super(ArticlePostCreateView, self).get_context_data(**kwargs)
        category2 = ArticleCategory.objects.order_by('title')
        ctx['categories'] = category2
        return ctx

def article_details(request, slug):
    post = get_object_or_404(ArticlePost, slug=slug)
    category2 = ArticleCategory.objects.order_by('title')
    posts = ArticlePost.objects.filter(approved=True)
    similiar_articles = list(set(ArticlePost.objects.filter(
        article_tags__name__in=list(
            post.article_tags.all())
    )))
    context = {
        "post": post,
        "categories": category2,
        "posts": posts,
        "similiar_articles": similiar_articles,
    }
    return render(request, 'articles/detail.html', context)
