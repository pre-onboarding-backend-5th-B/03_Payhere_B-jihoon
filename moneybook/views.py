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
        if user_moneybook_log.is_active:
            return Response(
                {
                    "msg": request.user.name,
                    "log": MoneyBookLogReadSerializer(user_moneybook_log).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response({"msg":"this log is not activated"}, status=status.HTTP_403_FORBIDDEN)
    # 수정과 삭제(실제 METHOD는 PUT 이지만 is_active 를 수정해 접근 못하도록 구현)기능.
    def put(self, request, log_id):
        user_id = request.user.id
        user_moneybook = MoneyBook.objects.get(user=user_id)
        user_moneybook_log = MoneyBookLog.objects.get(
            moneybook=user_moneybook, log_id=log_id
        )
        # 해당 로그가 is_active = True 일때만 수정.
        if user_moneybook_log.is_active:
            serializer = MoneyBookLogCreateSerializer(user_moneybook_log, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"msg":"success",
                                "log":serializer.data},
                                status=status.HTTP_200_OK)
        return Response({"msg":"this log is not activated"}, status=status.HTTP_403_FORBIDDEN)
