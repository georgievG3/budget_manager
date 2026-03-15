from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, TransactionViewSet, ExpenseByCategoryView, IncomeByCategoryView

router = DefaultRouter()
router.register(r'wallets', WalletViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("stats/expenses-by-category/", ExpenseByCategoryView.as_view()),
    path("stats/income-by-category/", IncomeByCategoryView.as_view()),
]