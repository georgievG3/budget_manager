
from django.utils import timezone
from django.db.models import Sum
from django.db import models
from django.conf import settings
from django.forms import ValidationError

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s wallet"
    
class Category(models.Model):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

    CATEGORY_TYPES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="categories"
    )

    def __str__(self):
        return self.name


class Transaction(models.Model):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

    TRANSACTION_TYPES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.amount}"
    
    
    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Amount should be greater than 0!!!")
        
        if self.pk:
            old = Transaction.objects.get(pk=self.pk)
            if old.wallet != self.wallet:
                raise ValidationError("Changing wallet is not allowed.")
            
        if self.category and self.type:
            if self.category.type != self.type:
                raise ValidationError('Category type must match transaction type!!!')
            
        if self.category.user and self.category.user != self.wallet.user:
                raise ValidationError("Category does not belong to this user.")
        
        if self.type == "EXPENSE" and self.category:
            today = timezone.now()

            month = today.month
            year = today.year

            budget = Budget.objects.filter(
                user=self.wallet.user,
                category=self.category,
                month=month,
                year=year
            ).first()

            if budget:
                total_spent = Transaction.objects.filter(
                    wallet=self.wallet,
                    category=self.category,
                    type="EXPENSE",
                    created_at__month=month,
                    created_at__year=year
                ).aggregate(total=Sum("amount"))["total"] or 0

                if total_spent + self.amount > budget.limit:
                    raise ValidationError("You exceeded your budget for this category.")

            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Budget(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.category.name} - {self.limit} ({self.month}/{self.year})"
    
    def clean(self):
        if Budget.objects.filter(
            user=self.user,
            category=self.category,
            month=self.month,
            year=self.year
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Budget already exists for this category and month!")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)