from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from moneybook.models import MoneyBook, MoneyBookLog
from moneybook.serializers import (
    MoneyBookLogCreateSerializer,
    MoneyBookLogReadSerializer,
)

# Create your views here.


class MoneyBookLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        user_moneybook = MoneyBook.objects.get(user=user_id)
        user_moneybook_log = MoneyBookLog.objects.filter(moneybook=user_moneybook.id)
        print(user_moneybook_log)
        return Response(
            MoneyBookLogCreateSerializer(user_moneybook_log, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        user_id = request.user.id
        user_moneybook = MoneyBook.objects.get(user=user_id)

        log_id = user_moneybook.latest_log_id + 1

        request_dic = request.data
        request_dic["log_id"] = log_id
        request_dic["moneybook"] = user_moneybook.id

        serializer = MoneyBookLogCreateSerializer(data=request_dic)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_moneybook.latest_log_id += 1
            user_moneybook.save()
            return Response({"msg": serializer.data}, status=status.HTTP_201_CREATED)


class MoneyBookLogDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, log_id):
        user_id = request.user.id
        user_moneybook = MoneyBook.objects.get(user=user_id)
        user_moneybook_log = MoneyBookLog.objects.get(
            moneybook=user_moneybook, log_id=log_id
        )
        return Response(
            {
                "msg": request.user.name,
                "log": MoneyBookLogReadSerializer(user_moneybook_log).data,
            },
            status=status.HTTP_200_OK,
        )
