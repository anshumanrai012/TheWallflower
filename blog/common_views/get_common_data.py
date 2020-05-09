from blog.models import Post, Author, Tag, Follow, PostLike, PostView, Follow, PostLike, PostComment
from django.contrib.auth.models import User

GENDER_CHOICES = {'m': 'Male', 'f': 'Female', 'o': 'Others'}


def get_gender_name_by_value(value):
    return GENDER_CHOICES[value]


def get_post_view_status(userid, postid):
    is_viewed = False
    viewed_post = PostView.objects.filter(post_id=postid, viewed_by_id=userid)
    if viewed_post:
        is_viewed = True
    return is_viewed


def get_tag_id_by_name(name):
    tag_id = Tag.objects.filter(name=name).values('id')[0]['id']

    return tag_id


def get_user_id_by_username(u_name):
    user_id = User.objects.filter(username=u_name).values('id')[0]['id']
    return user_id


def get_views_count_by_post(post_id):
    view_count = PostView.objects.filter(post_id=post_id).count()
    return view_count


def get_views_count_by_author(author_id):
    total_views = 0
    posts = Post.objects.filter(author_id=author_id).values('id')
    for post in posts:
        post_id = post['id']
        view_count = PostView.objects.filter(post_id=post_id).count()
        total_views += view_count
    return total_views


def get_following_status(author_id, follower_id):
    is_following = False
    follower = Follow.objects.filter(author=author_id, follower=follower_id)
    if follower:
        is_following = True

    return is_following


def get_like_count_by_post(post_id):
    like_count = PostLike.objects.filter(post_id=post_id, is_liked=True).count()
    return like_count


def get_liked_status(post_id, liker_id):
    is_liked = False
    likes = PostLike.objects.filter(post_id=post_id, liked_by_id=liker_id, is_liked=True, is_unliked=False)
    if likes:
        is_liked = True

    return is_liked


def get_liked_but_unliked(post_id, liker_id):
    is_liked_but_unliked = False
    liked_but_unliked = PostLike.objects.filter(post_id=post_id, liked_by_id=liker_id, is_liked=False, is_unliked=True)
    if liked_but_unliked:
        is_liked_but_unliked = True
    return is_liked_but_unliked


def get_comments_by_post_id(post_id):
    posts = PostComment.objects.filter(id=post_id)
    return posts



