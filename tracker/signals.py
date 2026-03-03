from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from tracker.models import Transaction, Wallet



User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


@receiver(post_save, sender=Transaction)
def update_balance(sender, instance, created, **kwargs):
    if created:
        wallet=instance.wallet
        if instance.type == "INCOME":
            wallet.current_balance += instance.amount
        else:
            wallet.current_balance -= instance.amount
        wallet.save()
            
