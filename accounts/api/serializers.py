from accounts.models import CustomUser, Follow
from rest_framework import serializers



class CustomUserSerializer(serializers.ModelSerializer):
     class Meta:
         model = CustomUser
         fields = ['id', 'email', 'username', 'age', 'date_of_birth', 'image']
         read_only_fields = ['id']


class FollowSerializer(serializers.ModelSerializer):
    # this is one way to show the user's username( and then we use get_field method)
    follower = serializers.SerializerMethodField()
    # and this is another way which in my favorite
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'user', 'created_at']

    def get_follower(self, obj):
        return obj.follower.username