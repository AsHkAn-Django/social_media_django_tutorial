from rest_framework import serializers
from myApp.models import Post, Comment, Like



class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'created_at']

    def get_author(self, obj):
        return obj.author.username
