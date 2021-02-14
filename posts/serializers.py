from rest_framework import serializers
from .models import Comment


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data





# class NestedCommentSerializer(serializers.ModelSerializer):
#     reply_comment = serializers.SerializerMethodField()
#     username = serializers.SerializerMethodField()
#     image_url = serializers.SerializerMethodField()
#
#     def get_reply_comment(self, obj):
#         if obj.reply_comment is not None:
#             return NestedCommentSerializer(obj.reply_comment).data
#         else:
#             return None
#
#     def get_username(self, obj):
#         return obj.user.username
#
#     def get_image_url(self, obj):
#         return obj.user.user_profile.profile_image.url
#
#     class Meta:
#         model = Comment
#         fields = '__all__'
#


class CommentNestedSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True, allow_null=True)
    username = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_image_url(self, obj):
        return obj.user.user_profile.profile_image.url

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True, allow_null=True)
    username = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()



    def get_username(self, obj):
        return obj.user.username

    def get_image_url(self, obj):
        return obj.user.user_profile.profile_image.url

    class Meta:
        model = Comment
        fields = '__all__'
