from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from .serializers import CustomUserSerializer, FollowSerializer
from myApp.api.serializer import PostSerializer
from accounts.models import Follow, CustomUser
from myApp.models import Post



class UserAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = CustomUser.objects.all()
        users = CustomUserSerializer(qs, many=True)
        return Response({'users': users.data})


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        """
        For getting the list of following users.
        """
        qs = Follow.objects.all()
        follows = FollowSerializer(qs, many=True)
        return Response({'follows': follows.data})

    def post(self, req):
        """
        For Following and unfollowing users.
        """
        serializer = FollowSerializer(data=req.data)
        if serializer.is_valid():
            follower = req.user
            following = serializer.validated_data['user']
            if follower == following:
                return Response({'Error': "You can't follow yourself!"},
                                status=status.HTTP_403_FORBIDDEN)
            follow_exist = Follow.objects.filter(follower=follower, user=following)
            if follow_exist.exists():
                follow_exist.delete()
                return Response({'message': f"{follower.username} unfollowed {following.username}."},
                                status=status.HTTP_204_NO_CONTENT)

            serializer.save(follower=req.user)
            return Response({'message': f"{follower.username} followed {following.username}."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        following_ids = Follow.objects.filter(follower=req.user).values_list('user_id', flat=True)
        posts = Post.objects.filter(author_id__in=following_ids).select_related('author').order_by('-created_at')
        serialized_posts = PostSerializer(posts, many=True)
        return Response(serialized_posts.data, status=status.HTTP_200_OK)

