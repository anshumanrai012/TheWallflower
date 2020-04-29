from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import pre_save
from django.utils import timezone
import pytz
from django.conf import settings
from django.http import request
from django.urls import reverse

# Create your models here.
from thewallflower.util import unique_slug_generator

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('a', 'Archived')
)

GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Others')
)


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    title = models.CharField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=1000, blank=True, null=True)
    post_content = models.TextField(max_length=1000000)
    summary = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='p')
    tag = models.ManyToManyField(Tag, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.slug)])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Post)


class Author(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    bio = models.TextField(max_length=2000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def get_author_for_posts(self):
        return reverse('posts-by-author', args=[str(self.id)])

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['name']


class PostView(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    viewed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_id


class PostLike(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(null=True)
    is_liked = models.BooleanField(null=True)
    unliked_at = models.DateTimeField(null=True)
    is_unliked = models.BooleanField(null=True)

    def __str__(self):
        return self.post_id


class PostComment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    comment_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.comment
