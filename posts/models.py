from django.db import models
from accounts.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, verbose_name="Post title")
    sub_title = models.CharField(max_length=500, null=True, blank=True, verbose_name="Subtitle")
    content = models.TextField(null=True, blank=True)
    like_num = models.IntegerField(default=0, verbose_name="Number of likes")
    comment_num = models.IntegerField(default=0, verbose_name="Number of comments")
    add_time = models.DateTimeField(auto_now=True, verbose_name="Post add time")

    def __str__(self):
        return self.title


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
    like_time = models.DateTimeField(auto_now=True, verbose_name="like time")


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_image")
    image = models.ImageField(upload_to='post_images/')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    content = models.TextField()
    add_time = models.DateTimeField(auto_now=True, verbose_name="comment add time", help_text="comment add time")
    parent_comment = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True,
                                       related_name="replies")
    comment_level = models.IntegerField(default=0)

    def __str__(self):
        return self.content
