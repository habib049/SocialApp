from rest_framework import serializers
from accounts.models import User


class UserListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.user_profile.profile_image.url

    class Meta:
        model = User
        fields = ['username', 'image_url']
