from django.contrib import admin
from .models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'phone', 'city', 'country']
    search_fields = ['get_username']


@admin.register(UserEducation)
class UserEducationAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'degree', 'description', 'start_date', 'end_date']
    search_fields = ['get_username']


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']
    search_fields = ['name']


@admin.register(UserPrivacy)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'profile_image', 'date_of_birth', 'phone_number', 'friends', 'search']
    search_fields = ['get_username']


@admin.register(UserHobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'get_hobby_name']
    search_fields = ['get_username']
