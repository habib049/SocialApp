from django.contrib import admin
from .models import  Post, PostImage,Comment



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'add_time','comment_level']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'sub_title', 'content']
    search_fields = ['title']


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['get_post', 'image']

    def get_post(self, obj):
        return obj.post.title
