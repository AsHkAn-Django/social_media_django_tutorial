from rest_framework.views import APIView
from .serializers import CustomUserSerializer, FollowSerializer
from accounts.models import Follow, CustomUser
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated



class UserAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = CustomUser.objects.all()
        users = CustomUserSerializer(qs, many=True)
        return Response({'users': users.data})


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        qs = Follow.objects.all()
        follows = FollowSerializer(qs, many=True)
        return Response({'follows': follows.data})

