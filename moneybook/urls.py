from django.urls import path
from moneybook import views

urlpatterns = [
    path("", views.MoneyBookLogAPIView.as_view(), name="moneybook"),
]
