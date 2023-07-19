from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from author.models import Author
from datetime import datetime


class DiaryPost(models.Model):
    title = models.CharField(max_length=400)
    slug = models.CharField(max_length=400, unique=True, blank=True)
    diary_user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="diary_user")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True, unique=True, blank=False)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(datetime.now())[:10])
        super(DiaryPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        print("absolute url has been gotten")
        return reverse("diary_details", kwargs={
            "slug": self.slug
    })