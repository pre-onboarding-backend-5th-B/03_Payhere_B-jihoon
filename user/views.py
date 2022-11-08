from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Create your views here.
from .models import User
from .serializers import UserSerializer


class SignUpView(APIView):

    def post(self, request):
        data = request.data

        qs = User.objects.filter(email=request.data['email']) # TODO: serializer 에서 처리
        if qs.exists():
            return Response({"msg":"email exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "signup success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },

                },
                status=status.HTTP_201_CREATED
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"msg":"test pass"}, status=status.HTTP_200_OK)

