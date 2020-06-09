from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import auth_logout
from . import views

# URLs for Homepage

urlpatterns = [
    path('', views.index, name='index'),
]

# URLs for Post
urlpatterns += [
    path('blog/posts', views.PostListView.as_view(), name='all-posts'),
    path('blog/post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('blog/post/new-post', views.PostCreate.as_view(), name='new-post'),
    path('blog/posts/search/', views.PostSearchListView.as_view(), name='post-search-list-view'),
    path('blog/tags/', views.TagListView.as_view(), name='all-tags'),
    path('blog/archives/', views.get_all_archives, name='archives'),
    path('post/<slug:slug>/like', views.like_post, name='like-post'),
    path('post/<slug:slug>/unlike', views.unlike_post, name='unlike-post'),
    path('post/<slug:slug>/comment', views.add_new_comment, name='add-comment'),
    path('post/comment/<int:pk>/', views.add_new_reply, name='add-reply'),
    path('post/comment/<int:pk>/delete', views.delete_a_comment, name='delete-comment'),
    path('post/reply/<int:pk>/delete', views.delete_a_reply, name='delete-reply'),
    path('post/bookmark/<int:pk>/', views.bookmark_a_post, name='bookmark-post')

]

# URLs for Author
urlpatterns += [
    path('account/activate/', views.AuthorCreate.as_view(), name='activate-account'),
    path('blog/authors/', views.AuthorListView.as_view(), name='all-authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/edit/<int:pk>/', views.AuthorUpdateView.as_view(), name='author_edit'),
    path('blog/authors/search/', views.AuthorSearchListView.as_view(), name='author-search-list-view'),
    path('blog/tags/', views.TagListView.as_view(), name='all-tags'),
    path('blog/<slug:user>/follow/', views.add_new_follower, name='new-follow'),
    path('blog/<slug:user>/unfollow/', views.remove_follower, name='unfollow'),
]

# URLs for Tags
urlpatterns += [
    path('blog/tags/', views.TagListView.as_view(), name='all-tags'),
]

# URLs for Profile
urlpatterns += [
    path('blog/<slug:user>/', views.user_profile, name='profile'),
    path('blog/post/<int:pk>/edit', views.PostUpdateView.as_view(), name='update-post'),
    path('blog/post/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete-post'),
    path('blog/post/<int:pk>/archived', views.mark_post_archive, name='mark-archive'),
    path('blog/post/<int:pk>/restored', views.mark_post_unarchive, name='mark-restore'),
    path('blog/<int:pk>/edit/', views.AuthorUpdateView.as_view(), name='edit-profile')
]

urlpatterns += [
    path('blog/posts/<slug:item>/', views.get_post_by_tag, name='posts-by-tag'),
]
