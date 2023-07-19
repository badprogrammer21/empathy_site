from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
from django.db.models import Count, Sum
from author.models import Author
import schedule


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default="description")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.title  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("posts", kwargs={
            "slug": self.slug
        })
    
    @property
    def num_posts(self):
        Post.objects.filter(categories=self).count()

    @property
    def last_post(self):
        Post.objects.filter(categories=self).latest("date")


class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.content[:100]
    
    class Meta:
        verbose_name_plural = "replies"

class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)

    def __str__(self) -> str:
        return self.content[:100]
    

class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.CharField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    categories = models.ManyToManyField(Category)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field="object_pk",
                                            related_query_name="hit_count_generic_relation")
    tags = TaggableManager(related_name="forum_tags")
    comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        print("hjello")
        print("absolute url has been gotten")
        return reverse("details", kwargs={
            "slug": self.slug
        })