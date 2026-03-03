from django.contrib import admin
from .models import Wallet, Transaction, Category

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Category)