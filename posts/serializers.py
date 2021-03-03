from rest_framework import serializers
from .models import Comment, PostLike


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True, allow_null=True)
    username = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()

    def get_post_id(self, obj):
        return obj.post.id

    def get_username(self, obj):
        return obj.user.username

    def get_image_url(self, obj):
        return obj.user.user_profile.profile_image.url

    class Meta:
        model = Comment
        fields = '__all__'


class LikeListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_image_url(self, obj):
        return obj.user.user_profile.profile_image.url

    class Meta:
        model = PostLike
        fields = ['username', 'image_url']
