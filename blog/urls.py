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
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new-post', views.PostCreate.as_view(), name='new-post'),
    path('blog/posts/search/', views.PostSearchListView.as_view(), name='post-search-list-view'),
    path('blog/tags/', views.TagListView.as_view(), name='all-tags'),

]

# URLs for Author
urlpatterns += [
    path('profile/', views.AuthorCreate.as_view(), name='edit-profile'),
    path('blog/authors/', views.AuthorListView.as_view(), name='all-authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/edit/<int:pk>/', views.AuthorUpdateView.as_view(), name='author_edit'),
    path('blog/authors/search/', views.AuthorSearchListView.as_view(), name='author-search-list-view'),
    path('blog/tags/', views.TagListView.as_view(), name='all-tags'),
]

# URLs for Tags
urlpatterns += [
    path('blog/tags/', views.TagListView.as_view(), name='all-tags'),
]

# URLs for Profile
urlpatterns += [
    path('blog/profile/', views.user_profile, name='profile'),
    path('blog/post/<int:pk>/edit', views.PostUpdateView.as_view(), name='update-post'),
    path('blog/post/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete-post')



]
