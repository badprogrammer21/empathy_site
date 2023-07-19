from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout as lg
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages, auth
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from author.models import Author
from forum.models import Post, Category
from article.models import ArticlePost as ArticlePost
from article.models import ArticleCategory as ArticleCategory
from diary.models import DiaryPost
from forum.utils import update_views
from django.contrib import messages
from django.db.models import Count
from taggit.models import Tag


def home(request):
    #forums = Category.objects.all()
    user = request.user
    context = {
        #"forums": forums,
        "user": user,
    }
    return render(request, 'main.html', context)

def articles(request):
    category = ArticleCategory.objects.order_by('title')
    posts = ArticlePost.objects.all()
    posts_iter = Paginator(posts, 4)
    post = request.GET.get('page')
    paged_posts = posts_iter.get_page(post)
    tags = list(set([tag for post in posts for tag in post.article_tags.all()]))[:10]
    context = {
        "category": category,
        "posts": paged_posts,
        "topics": tags,
    }
    return render(request, 'articles/articles.html', context)

from datetime import datetime, timezone
def diary(request):
    return render(request, 'diary/diary.html',{
                      'posts': DiaryPost.objects.order_by('date'),
                      'days_from_latest_post': (datetime.now(timezone.utc)-DiaryPost.objects.latest('date').date).days,
                      })


def forum(request):
    category = Category.objects.order_by('title')
    posts = Post.objects.filter(approved=True)
    posts_iter = Paginator(posts, 6)
    post = request.GET.get('page')
    paged_posts = posts_iter.get_page(post)
    all_posts = Post.objects.filter(approved=True)
    fx=[len(Post.objects.filter(categories=cat)) for cat in category]
    context = {
        "categories": category,
        "posts": paged_posts,
        "all_posts": all_posts,
        "cats": zip(category, fx)
    }
    
    return render(request, 'forum/forum.html', context)

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'You are now logged in')
            return redirect('login')
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = UserRegisterForm()
    return render(request, 'registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('create_profile', user.id)
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')
    
def logout(request):
    lg(request)
    messages.success(request, 'You are now logged out')
    return redirect('login')


@login_required
def create_profile(request, user_id):
    print(user_id)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.author)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile', user_id)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.author)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_id': user_id,
    }
    return render(request, 'profile/profile.html', context)

def profile(request, id_user):
    try:
        pf_user = User.objects.get(id=id_user)
    except:
        raise Http404("User not found")
    print(pf_user.author.bio)
    return render(request, 'profile/profile.html', {
        'users_forum_posts': Post.objects.filter(user=pf_user.author),
        'users_article_posts': ArticlePost.objects.filter(article_users=pf_user.author),
        'another_user': request.user,
        'user': pf_user,
        'lst': [
            len(Post.objects.filter(user=pf_user.author)),
            len(ArticlePost.objects.filter(article_users=pf_user.author))
        ]
    })

@login_required
def edit_profile(request):
    author = Author.objects.get(user=request.user)
    if request.method == 'POST':
        old_pass = request.user.password
        ps1, ps2 = request.POST['password'], request.POST['password2']
        userform = UserUpdateForm(request.POST,instance=request.user)
        profileform = ProfileUpdateForm(request.POST,request.FILES,instance=author)
        choice = request.POST.getlist("ph")
        if userform.is_valid() and profileform.is_valid():
            if ps1 == ps2:
                users_password = request.user
                new_profile = profileform.save(commit=False)
                new_profile.user = request.user
                if "partially_hidden" in choice:
                    new_profile.hidden_profile = True
                if "partially_hidden" not in choice:
                    new_profile.hidden_profile = False
                if "completely_hidden" in choice:
                    new_profile.hidden = True
                if "completely_hidden" not in choice:
                    new_profile.hidden = False
                print(new_profile.bio)
                new_profile.save()
                userform.save()
                users_password.set_password(ps1)
                return redirect('profile', request.user.id)
            return redirect('forum')
    else:
        userform = UserUpdateForm(instance=request.user)
        profileform = ProfileUpdateForm(instance=author)
    
    return render(request,'profile/profile.html',context={'form1':userform,'form2':profileform})


"""
def news(request):
    category = Category.objects.order_by('title')
    posts = Post.objects.all()
    posts_iter = Paginator(posts, 6)
    post = request.GET.get('page')
    paged_posts = posts_iter.get_page(post)
    context = {
        "category": category,
        "posts": paged_posts,
    }
    return render(request, 'news.html', context)

def articles(request):
    category = Category.objects.order_by('title')
    posts = Post.objects.all()
    posts_iter = Paginator(posts, 6)
    post = request.GET.get('page')
    paged_posts = posts_iter.get_page(post)
    context = {
        "category": category,
        "posts": paged_posts,
    }
    return render(request, 'articles.html', context)
"""