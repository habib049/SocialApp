from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostCreateView.as_view(), name="create_post"),
    path('get-comments', views.CommentList.as_view(), name="more_comments"),
    path('post-new-comment', views.post_new_comment, name="post_new_comment"),
    path('post-reply-comment', views.post_reply_comment, name="post_reply_comment"),
    path('like-post',views.update_post_like,name="like_post"),
]
