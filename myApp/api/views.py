from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from myApp.models import Post, Comment, Like
from .serializer import PostSerializer



class PostAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req):
        qs = Post.objects.all()
        serialized_posts = PostSerializer(qs, many=True)
        return Response({"posts": serialized_posts.data}, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = PostSerializer(data=req.data)
        if serializer.is_valid():
            post = serializer.save(author=req.user)
            return Response({"Success": "New post has been created!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)