from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.generics import ListAPIView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from .serializers import CommentSerializer, LikeListSerializer
from django.views.generic import CreateView
from .forms import PostForm, PostWithImages
from .models import Post, PostImage, Comment, PostLike


class PostCreateView(CreateView):
    model = Post
    form_class = PostWithImages
    template_name = 'home/create_post.html'
    success_url = reverse_lazy('home:home')

    def post(self, request, *args, **kwargs):
        new_post = PostForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')

        if new_post.is_valid():
            title = new_post.cleaned_data['title']
            sub_title = new_post.cleaned_data['sub_title']
            content = new_post.cleaned_data['content']

            # creating and saving post object
            post_object = Post.objects.create(user=request.user, title=title, sub_title=sub_title, content=content)

            # creating and saving post images
            for image in images:
                PostImage.objects.create(post=post_object, image=image)

            return redirect(reverse_lazy('home:home'))
        else:
            return self.form_invalid(new_post)


class CommentList(ListAPIView):
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        post_id = request.GET['post_id']
        post_id = str(post_id).split('-')[-1]
        queryset = Comment.objects.filter(post_id=post_id, comment_level=0)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({'comments': serializer.data})


class LikeUserList(ListAPIView):
    serializer_class = LikeListSerializer

    def list(self, request, *args, **kwargs):
        post_id = request.GET['postId']
        queryset = PostLike.objects.filter(post_id=post_id)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({'users': serializer.data})


def post_new_comment(request):
    if request.method == 'POST' and request.is_ajax():
        comment_text = request.POST['comment']
        post_id = request.POST['post']
        post = Post.objects.get(id=post_id)
        post.comment_num += 1
        post.save()
        new_comment = Comment.objects.create(user=request.user, post=post, content=comment_text, comment_level=0)
        new_comment.save()
        return JsonResponse({'saved': 1})


def post_reply_comment(request):
    if request.method == 'POST' and request.is_ajax():
        parent_comment_id = request.POST['parentId']
        comment_text = request.POST['comment']
        parent_comment = Comment.objects.get(id=parent_comment_id)
        post = parent_comment.post
        post.comment_num += 1
        post.save()
        reply_comment = Comment.objects.create(user=request.user, parent_comment=parent_comment, post=post,
                                               content=comment_text, comment_level=parent_comment.comment_level + 1)
        reply_comment.save()
        return JsonResponse({'saved': 1})


def update_post_like(request):
    if request.method == 'POST' and request.is_ajax():
        post_id = request.POST['postId']
        try:
            like_entry = PostLike.objects.get(post_id=post_id, user=request.user)
            post = Post.objects.get(id=post_id)
            post.like_num -= 1
            post.save()
            like_entry.delete()
            return JsonResponse({'update': False, 'likes': post.like_num})
        except ObjectDoesNotExist:
            post = Post.objects.get(id=post_id)
            like_entry = PostLike.objects.create(post=post, user=request.user)
            post.like_num += 1
            post.save()
            like_entry.save()
            return JsonResponse({'update': True, 'likes': post.like_num})


