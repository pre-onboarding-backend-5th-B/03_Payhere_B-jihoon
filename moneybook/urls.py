from django.urls import path
from moneybook import views

urlpatterns = [
    path("", views.MoneyBookLogAPIView.as_view(), name="moneybook"),
    path(
        "<int:log_id>/", views.MoneyBookLogDetailAPIView.as_view(), name="moneybook_log"
    ),
]
