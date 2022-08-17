from django.contrib import admin
from .models import Profile, Post, Comment

admin.site.site_header = 'Rajat Administration'
admin.site.site_title = 'Rajat Administration'


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'body']
