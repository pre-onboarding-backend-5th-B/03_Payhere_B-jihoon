from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

# Create your models here.


class MoneyBook(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cash_amount = models.IntegerField(default=0)
    latest_log_id = models.IntegerField(default=0)


class MoneyBookLog(models.Model):
    MONEY_STATUS_CHOICES = (
        ("IC", "income"),
        ("EP", "Expense"),
    )
    log_id = models.IntegerField()
    moneybook = models.ForeignKey(MoneyBook, on_delete=models.CASCADE)
    cash = models.IntegerField(
        validators=[MinValueValidator(0)], default=0, help_text="수입/지출 금액"
    )
    money_status = models.CharField(
        max_length=2, choices=MONEY_STATUS_CHOICES, blank=False, null=False
    )
    memo = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
