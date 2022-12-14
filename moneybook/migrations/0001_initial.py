# Generated by Django 4.1.3 on 2022-11-06 09:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MoneyBook",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cash_amount", models.IntegerField(default=0)),
                ("latest_log_id", models.IntegerField(default=0)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MoneyBookLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("log_id", models.IntegerField()),
                (
                    "cash",
                    models.IntegerField(
                        default=0,
                        help_text="수입/지출 금액",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "money_status",
                    models.CharField(
                        choices=[("IC", "income"), ("EP", "Expense")], max_length=2
                    ),
                ),
                ("memo", models.CharField(blank=True, max_length=200)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "moneybook",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="moneybook.moneybook",
                    ),
                ),
            ],
        ),
    ]
