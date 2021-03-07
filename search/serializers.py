from rest_framework import serializers
from accounts.models import User
from posts.models import Post


class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.user_profile.profile_image.url

    def get_city(self, obj):
        return obj.user_profile.city

    def get_country(self, obj):
        return obj.user_profile.country

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name','city','country', 'image_url']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
