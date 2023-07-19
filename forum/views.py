from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView
from .models import Post, Category, Author, Comment
from .utils import update_views
from django.utils.decorators import method_decorator
from django import template
from .forms import PostForm


def category_posts(request, slug):
    category = Category.objects.order_by('title')
    category2 = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category2)
    context = {
        "all_categories": category,
        "posts": posts,
        "cats": zip(
            category,
            [len(Post.objects.filter(categories=cat)) for cat in category]
        ),
    }
    return render(request, 'forum/category_posts.html', context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    category2 = Category.objects.order_by('title')
    posts = Post.objects.filter(approved=True)
    user = request.user
    if "comment" in request.POST:
        comment = request.POST.get("comment")
        print(request.POST)
        new_comment, created = Comment.objects.get_or_create(user=user.author, content=comment)

        post.comments.add(new_comment.id)

    if "reply" in request.POST:
        reply = request.POST.get("reply")

    if "post_edit" in request.POST:
        pst = request.POST.get("post_edit")
        post.content = pst
        post.save()

    if "title_edit" in request.POST:
        pst = request.POST.get("title_edit")
        post.title = pst
        post.slug = '-'.join(pst.split()).lower().strip()
        post.save()
        return redirect("details", slug=post.slug)
    category = Category.objects.order_by("title")
    context = {
        "user": user,
        "categories": category2,
        "post": post,
        "posts": posts,
        "cats": zip(
            category,
            [len(Post.objects.filter(categories=cat)) for cat in category]
        ),
    }
    update_views(request, post)
    return render(request, 'forum/detail.html', context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    category2 = Category.objects.order_by('title')
    
    context = {
        "categories": category2,
        "posts": posts,
    }
    return render(request, 'forum/posts.html', context)

def new_forum(request):
    category2 = Category.objects.order_by('title')
    context = {
        "categories": category2,
    }
    return render(request, 'forum/new_forum.html', context)

def search_forum_post(request):
    category = Category.objects.order_by('title')
    queryset_list = Post.objects.filter(approved=True)
    all_posts = Post.objects.all()
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(content__icontains=keywords)
    return render(request, 'forum/search.html', {
        'posts_search': queryset_list,
        'categories': category,
        'all_posts': all_posts,
        "cats": zip(
            category,
            [len(Post.objects.filter(categories=cat)) for cat in category]
        ),
    })



class PostCreateView(CreateView):
    model = Post
    template_name = 'forum/new_forum.html'
    form_class = PostForm

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.user = Author.objects.get(user=self.request.user)
        candidate.save()
        return super(PostCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(PostCreateView, self).get_context_data(**kwargs)
        category2 = Category.objects.order_by('title')
        ctx['categories'] = category2
        return ctx
