from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView
from .models import DiaryPost, Author
from django.utils.decorators import method_decorator
from django import template
from taggit.models import Tag
from .forms import DiaryPostForm


def diary_details(request, slug):
    post = get_object_or_404(DiaryPost, slug=slug)
    posts = DiaryPost.objects.latest('date')
    context = {
        "post": post,
        "posts": posts,
    }
    return render(request, 'diary/detail.html', context)

from datetime import datetime, timezone
class DiaryPostCreateView(CreateView):
    model = DiaryPost
    template_name = 'diary/new_diary.html'
    form_class = DiaryPostForm

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.diary_user = Author.objects.get(user=self.request.user)
        candidate.save()
        return super(DiaryPostCreateView, self).form_valid(form)
    
    def form_invalid(self):
        return redirect('login')