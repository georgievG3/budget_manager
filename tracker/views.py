from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.response import Response
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer

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