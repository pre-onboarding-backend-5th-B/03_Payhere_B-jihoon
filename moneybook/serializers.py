from rest_framework import serializers

from moneybook.models import MoneyBook, MoneyBookLog


class MoneyBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBook
        fields = "__all__"


class MoneyBookLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBookLog
        fields = "__all__"
