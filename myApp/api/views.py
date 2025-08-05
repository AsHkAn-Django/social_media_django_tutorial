from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import CursorPagination

from django.shortcuts import get_object_or_404

from myApp.models import Post, Comment, Like
from .serializer import PostSerializer



class PostAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req, pk=None):
        if pk is not None:
            post = get_object_or_404(Post, pk=pk)
            serialized_post = PostSerializer(post, many=False)
            return Response({'detail': serialized_post.data}, status=status.HTTP_200_OK)
        qs = Post.objects.all().order_by('-created_at')
        paginator = CursorPagination()
        paginator.ordering = '-created_at'
        paginated_qs = paginator.paginate_queryset(qs, request=req)
        serialized_posts = PostSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serialized_posts.data)

    def post(self, req):
        serializer = PostSerializer(data=req.data)
        if serializer.is_valid():
            post = serializer.save(author=req.user)
            return Response({"success": "New post has been created!"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, pk=None):
        if pk is None:
            return Response({"error": "Post ID is required for deletion."},
                            status=status.HTTP_400_BAD_REQUEST)
        post = get_object_or_404(Post, pk=pk)
        if post.author != req.user:
            return Response({"error": "You do not have permission to delete this post."},
                            status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"success": "Post has been deleted"}, status=status.HTTP_204_NO_CONTENT)



