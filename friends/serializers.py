from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.friend.username

    def get_user_id(self, obj):
        return obj.friend.id

    def get_city(self, obj):
        return obj.friend.user_profile.city

    def get_country(self, obj):
        return obj.friend.user_profile.country

    def get_image_url(self, obj):
        return obj.friend.user_profile.profile_image.url

    class Meta:
        model = User
        fields = ['user_id', 'username', 'image_url', 'city', 'country']
