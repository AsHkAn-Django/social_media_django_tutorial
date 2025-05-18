from django.contrib import admin
from .models import Post, Like, Comment
from mptt.admin import MPTTModelAdmin


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('body','created_at', 'parent')
    mptt_level_indent = 20  # pixels to indent per level
    

admin.site.register(Post)
admin.site.register(Like)