from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.response import Response
from .models import Budget, Wallet, Transaction
from .serializers import BudgetSerializer, WalletSerializer, TransactionSerializer

class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer



class ExpenseByCategoryView(APIView):

    def get(self, request):
        user = request.user

        data = (
            Transaction.objects.filter(
                wallet__user=user, type="EXPENSE"
            ).values(
                "category__name"
            ).annotate(
                total=Sum('amount')
            ).order_by(
                "-total"
            )
        )

        return Response(data)
    

class IncomeByCategoryView(APIView):

    def get(self, request):

        user = request.user

        data = (
            Transaction.objects.filter(
                wallet__user=user, type="INCOME"
            ).values(
                "category__name"
            ).annotate(
                total=Sum('amount')
            ).order_by(
                "-total"
            )
        )

        return Response(data)
    

class DashboardView(APIView):

    def get(self, request):
        user = request.user
        current_balance = user.wallet.current_balance
        total_expenses = Transaction.objects.filter(wallet__user=user, type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
        total_income = Transaction.objects.filter(wallet__user=user, type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
        last_five_transactions = Transaction.objects.filter(wallet__user=user).order_by("-created_at")[:5]
       


        return Response({
            "current_balance": current_balance,
            "total_expenses": total_expenses,
            "total_income": total_income,
            "last_5_transactions": TransactionSerializer(last_five_transactions, many=True).data,
            })
    

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()  
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)