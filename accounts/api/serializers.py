from accounts.models import CustomUser, Follow
from rest_framework import serializers



class CustomUserSerializer(serializers.ModelSerializer):
    num_of_posts = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'age', 'date_of_birth', 'image', 'num_of_posts']
        read_only_fields = ['id', 'num_of_posts']

    def get_num_of_posts(self, obj):
        return obj.posts.count()


class FollowSerializer(serializers.ModelSerializer):
    # this is one way to show the user's username( and then we use get_field method)
    follower = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'user', 'created_at']
        read_only_fields = ['id', 'follower']

    def get_follower(self, obj):
        return obj.follower.username

    def get_user(self, obj):
        return obj.user.username