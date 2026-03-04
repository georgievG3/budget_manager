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
            
        if self.category.user != self.wallet.user:
            raise ValidationError("Category does not belong to this user.")

            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)