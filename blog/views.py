from functools import reduce
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from .models import Post, Author, Tag
from .forms import AuthorForm
from django.contrib.auth.mixins import LoginRequiredMixin
import operator
from django.db.models import Q
from django.conf import settings


def index(request):
    num_posts = Post.objects.all().count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_posts': num_posts, 'num_authors': num_authors, 'num_visits': num_visits},
    )


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'post_content', 'summary', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    paginate_by = 10


class PostSearchListView(PostListView):
    paginate_by = 10

    def get_queryset(self):
        result = super(PostSearchListView, self).get_queryset()
        query = self.request.GET.get('qery')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(post_content__icontains=q) for q in query_list))
            )

        return result


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        posts = Post.objects.filter(author=self.object.author).values('id', 'author', 'title', 'slug')
        for post in posts:
            ids = post['author']

        context['author'] = Author.objects.filter(username=ids).values('name', 'bio')
        context['authors_posts'] = posts

        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'post_content', 'summary']
    login_url = 'login'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('profile')
    login_url = 'login'


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    template_name = 'blog/author_form.html'
    fields = ('username', 'name', 'email')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)


class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'blog/author_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        print(self.object)
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        post_count_by_author = Post.objects.filter(author_id=self.object.username_id).count()
        posts = Post.objects.filter(author_id=self.object.username_id).values('id', 'title', 'post_content', 'summary',
                                                                              'created_at')
        context['authors_posts'] = posts
        context['post_count_by_author'] = post_count_by_author
        return context


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    template_name = 'blog/author_edit.html'
    fields = ('username', 'name', 'email')
    login_url = 'login'


class AuthorListView(ListView):
    model = Author
    paginate_by = 10


class AuthorSearchListView(AuthorListView):
    paginate_by = 10

    def get_queryset(self):
        result = super(AuthorSearchListView, self).get_queryset()
        query = self.request.GET.get('qery')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(bio__icontains=q) for q in query_list))
            )

        return result


class TagListView(ListView):
    model = Tag
    paginate_by = 10


class TagDetailView(DetailView):
    model = Tag


def user_profile(request):
    user_id = User.objects.filter(username=request.user).values('id')[0]['id']
    posts = Post.objects.filter(author_id=user_id)
    num_posts = Post.objects.filter(author_id=user_id).count()
    author = Author.objects.filter(username_id=user_id).values('id', 'name', 'bio')

    return render(
        request,
        'blog/profile.html',
        context={'num_posts': num_posts, 'posts': posts, 'author': author},
    )
