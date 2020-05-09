from functools import reduce
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from .models import Post, Author, Tag, Follow, PostView, PostLike, PostComment, PostReply
from django.contrib.auth.mixins import LoginRequiredMixin
import operator
from django.db.models import Q, Count
from blog.common_views import get_common_data
from .forms import AuthorForm
from django.utils import timezone


def index(request):
    num_posts = Post.objects.all().count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    author_details = None

    if request.user.is_authenticated:
        user_id = User.objects.filter(username=request.user).values('id')[0]['id']
        author_details = Author.objects.filter(username_id=user_id)
        author_details_count = Author.objects.filter(username_id=user_id).count()

        if author_details_count == 1:
            fill_author_details = False
        else:
            fill_author_details = True

    else:
        fill_author_details = False

    if request.user.is_authenticated:
        user_id = get_common_data.get_user_id_by_username(request.user)
        lst_post_ids = []
        lst_followings = []
        posts_with_most_views = PostView.objects.values('post_id').annotate(Count('post_id')).order_by(
            '-post_id__count').values('post_id')
        for post in posts_with_most_views:
            lst_post_ids.append(post['post_id'])

        post_views = Post.objects.filter(id__in=lst_post_ids)
        followings = Follow.objects.filter(follower=int(user_id)).values('author', 'follower')
        for item in followings:
            lst_followings.append(item['author'])
        post_likes = Post.objects.filter(author_id__in=lst_followings)
        context = {'num_posts': num_posts, 'num_authors': num_authors, 'num_visits': num_visits,
                   'author_details': author_details, 'fill_author_details': fill_author_details,
                   'post_views': post_views, 'post_likes': post_likes}

    else:
        context = {'num_posts': num_posts, 'num_authors': num_authors, 'num_visits': num_visits,
                   'author_details': author_details, 'fill_author_details': fill_author_details,
                   }

    return render(
        request,
        'index.html',
        context,
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

    def get_queryset(self):
        return Post.objects.filter(status='p')


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


def save_view_record(post_id, Viewed_by_id):
    Follow.objects.create(post=Post)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        is_liked = False
        context = super(PostDetailView, self).get_context_data(**kwargs)
        posts = Post.objects.filter(author=self.object.author).values('id', 'author', 'title', 'slug')
        posts_obj = Post.objects.get(id=self.object.pk)
        post_id = Post.objects.filter(id=self.object.pk).values('id', 'author', 'title', 'slug')[0]['id']

        for post in posts:
            ids = post['author']

        context['author'] = Author.objects.filter(username=ids).values('name', 'bio')
        author_obj = User.objects.get(id=int(get_common_data.get_user_id_by_username(self.request.user)))
        context['authors_posts'] = posts
        context['username_id'] = ids

        if not get_common_data.get_post_view_status(int(get_common_data.get_user_id_by_username(self.request.user)),
                                                    post_id):
            PostView.objects.create(post=posts_obj, viewed_by=author_obj)

        if get_common_data.get_liked_status(post_id, int(get_common_data.get_user_id_by_username(self.request.user))):
            is_liked = True

        context['views_count'] = get_common_data.get_views_count_by_post(post_id)
        context['like_count'] = get_common_data.get_like_count_by_post(post_id)
        context['is_liked'] = is_liked
        context['comments'] = PostComment.objects.filter(post_id=self.object.pk, is_active=True).order_by('-comment_at')
        context['comment_count'] = PostComment.objects.filter(post_id=self.object.pk, is_active=True).count()
        comments = PostComment.objects.filter(post_id=self.object.pk, is_active=True).values('id')
        dict_replies = {}
        for comment in comments:
            dict_replies[comment['id']] = PostReply.objects.filter(comment_id=comment['id'], is_active=True)

        context['dict_replies'] = dict_replies

        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'post_content', 'summary', 'tag']
    template_name = 'blog/post_update_form.html'
    login_url = 'login'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('profile')
    login_url = 'login'


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['name', 'email', 'bio', 'gender']
    login_url = 'login'

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)


class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'blog/author_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        lst_followers = []
        lst_followings = []
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        post_count_by_author = Post.objects.filter(author_id=self.object.username_id).count()
        posts = Post.objects.filter(author_id=self.object.username_id)
        context['authors_posts'] = posts
        context['post_count_by_author'] = post_count_by_author
        context['author_id'] = self.object.username_id
        if get_common_data.get_following_status(self.object.username_id,
                                                get_common_data.get_user_id_by_username(self.request.user)):
            context['already_following'] = True
        else:
            context['already_following'] = False

        followers = Follow.objects.filter(author=int(self.object.username_id)).values('author', 'follower')
        for item in followers:
            lst_followers.append(item['follower'])

        context['followers_author_details'] = Author.objects.filter(username_id__in=lst_followers)
        followings = Follow.objects.filter(follower=int(self.object.username_id)).values('author', 'follower')
        for item in followings:
            lst_followings.append(item['author'])
        context['followings_author_details'] = Author.objects.filter(username_id__in=lst_followings)
        context['followers_count'] = Follow.objects.filter(author=int(self.object.username_id)).count()
        context['followings_count'] = Follow.objects.filter(follower=int(self.object.username_id)).count()
        context['total_view_count'] = get_common_data.get_views_count_by_author(int(self.object.username_id))
        context['likes_given'] = PostLike.objects.filter(liked_by_id=int(self.object.username_id))

        likes_given_count = PostLike.objects.filter(liked_by_id=int(self.object.username_id)).count()

        return context


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'blog/author_update_form.html'
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


def get_archives_by_author(request):
    user_id = get_common_data.get_user_id_by_username(request.user)
    archive_posts = Post.objects.filter(author_id=user_id, status='a')
    return archive_posts


def user_profile(request, user):
    lst_followers = []
    lst_followings = []
    lst_post_ids = []
    user_id = get_common_data.get_user_id_by_username(request.user)
    posts = Post.objects.filter(author_id=user_id, status='p')
    num_posts = Post.objects.filter(author_id=user_id).count()
    author = Author.objects.filter(username_id=user_id).values('id', 'name', 'bio', 'email', 'gender')
    gender = get_common_data.get_gender_name_by_value(author[0]['gender'])
    author_id = author[0]['id']
    archived_posts = get_archives_by_author(request)
    followers = Follow.objects.filter(author=int(user_id)).values('author', 'follower')
    for item in followers:
        lst_followers.append(item['follower'])

    followers_author_details = Author.objects.filter(username_id__in=lst_followers)
    followings = Follow.objects.filter(follower=int(user_id)).values('author', 'follower')
    for item in followings:
        lst_followings.append(item['author'])
    followings_author_details = Author.objects.filter(username_id__in=lst_followings)
    followers_count = Follow.objects.filter(author=int(user_id)).count()
    followings_count = Follow.objects.filter(follower=int(user_id)).count()
    total_view_count = get_common_data.get_views_count_by_author(user_id)
    liked_posts = PostLike.objects.filter(liked_by_id=user_id)
    likes_given_count = PostLike.objects.filter(liked_by_id=user_id).count()

    return render(
        request,
        'blog/profile.html',
        context={'num_posts': num_posts, 'posts': posts, 'author': author, 'archived_posts': archived_posts,
                 'gender': gender, 'author_id': author_id, 'followers': followers_author_details,
                 'followings': followings_author_details,
                 'total_view_count': total_view_count, 'followers_count': followers_count,
                 'followings_count': followings_count, 'liked_posts': liked_posts,
                 'likes_given_count': likes_given_count},
    )


def get_post_by_tag(request, item):
    posts_under_tag = []
    tag_id = get_common_data.get_tag_id_by_name(item)
    post_ids = Post.tag.through.objects.filter(tag_id=tag_id).values('post_id')
    for val in post_ids:
        post_item = Post.objects.filter(id=val['post_id'], status='p')
        if post_item:
            posts_under_tag.append(post_item)

    return render(
        request,
        'blog/posts_by_tag.html',
        context={'posts_under_tag': posts_under_tag, 'tag_name': item},
    )


def mark_post_archive(request, pk):
    posts = Post.objects.filter(id=pk)
    posts.update(status='a')
    return user_profile(request, request.user)


def mark_post_unarchive(request, pk):
    posts = Post.objects.filter(id=pk)
    posts.update(status='p')
    return user_profile(request, request.user)


def get_all_archives(request):
    archive_posts = Post.objects.filter(status='a')
    return render(
        request,
        'blog/archive_list.html',
        context={'post_list': archive_posts},
    )


def add_new_follower(request, user):
    Follow.objects.create(author=user,
                          follower=int(get_common_data.get_user_id_by_username(request.user)))
    return redirect(request.META['HTTP_REFERER'])


def remove_follower(request, user):
    Follow.objects.filter(author=user,
                          follower=int(get_common_data.get_user_id_by_username(request.user))).delete()
    return redirect(request.META['HTTP_REFERER'])


def like_post(request, slug):
    current_user = User.objects.get(id=int(get_common_data.get_user_id_by_username(request.user)))
    current_post = Post.objects.get(slug=slug)
    if get_common_data.get_liked_but_unliked(current_post, current_user):
        records = PostLike.objects.filter(post_id=current_post, liked_by_id=current_user, is_liked=False,
                                          is_unliked=True)
        records.update(is_liked=True, is_unliked=False, liked_at=timezone.now())
    else:
        PostLike.objects.create(post=current_post, liked_by=current_user, liked_at=timezone.now(), is_liked=True,
                                is_unliked=False)
    return redirect(request.META['HTTP_REFERER'])


def unlike_post(request, slug):
    current_user = User.objects.get(id=int(get_common_data.get_user_id_by_username(request.user)))
    current_post = Post.objects.get(slug=slug)
    posts = PostLike.objects.filter(post=current_post, liked_by=current_user, is_liked=True, is_unliked=False)
    posts.update(is_unliked=True, is_liked=False, unliked_at=timezone.now())
    return redirect(request.META['HTTP_REFERER'])


def add_new_comment(request, slug):
    current_user = User.objects.get(id=int(get_common_data.get_user_id_by_username(request.user)))
    current_post = Post.objects.get(slug=slug)
    PostComment.objects.create(post=current_post, comment_by=current_user, comment=request.POST['comment'], comment_at=timezone.now(), is_active=True)
    return redirect(request.META['HTTP_REFERER'])


def add_new_reply(request,  pk):
    current_user = User.objects.get(id=int(get_common_data.get_user_id_by_username(request.user)))
    current_comment = PostComment.objects.get(id=pk)
    PostReply.objects.create(comment=current_comment, replied_by=current_user, reply=request.POST['reply'], replied_at=timezone.now(), is_active=True)
    return redirect(request.META['HTTP_REFERER'])


def delete_a_comment(request, pk):
    comment = PostComment.objects.filter(id=pk)
    comment.update(is_active=False)
    replies = PostReply.objects.filter(comment_id=pk)
    replies.update(is_active=False)
    return redirect(request.META['HTTP_REFERER'])


def delete_a_reply(request, pk):
    reply = PostReply.objects.filter(id=pk)
    reply.update(is_active=False)
    return redirect(request.META['HTTP_REFERER'])


