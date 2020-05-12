from django.db import models
from datetime import datetime, date, timedelta
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

def format_date(date_obj):
	formatedDate = date_obj.strftime("%Y%m%d")
	return str(formatedDate)

class Transaction(models.Model):
    transact_id = models.BigAutoField(primary_key=True)
    transact_date = models.DateField(default=date.today, verbose_name="Transaction Date")
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="Owner")
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="Creator")

    def __str__(self):
        return str(self.transact_id)

    def get_absolute_url(self):
        return reverse('accounts:transaction_detail', kwargs={'pk': self.pk})

class TransactionDetails(models.Model):
    transactDet_id = models.BigAutoField(primary_key=True)
    transactDet_desc = models.CharField(default='', max_length = 250, verbose_name = "Desc.")
    rm = models.DecimalField(default = 0, decimal_places = 2, max_digits=10, null = True, blank=True, verbose_name = "RM")
    usd = models.DecimalField(default = 0, decimal_places = 2, max_digits=10, null = True, blank=True, verbose_name = "USD")
    rmb = models.DecimalField(default = 0, decimal_places = 2, max_digits=10, null = True, blank=True, verbose_name = "RMB")
    transaction = models.ForeignKey(Transaction, on_delete = models.CASCADE, related_name="transaction_details")

    def __str__(self):
        return str(self.transactDet_id)
    
    class Meta:
        verbose_name = 'Transaction Detail'
        verbose_name_plural = 'Transaction Details'


class Profile(models.Model):
    BHANTE = 1
    SAYALAY = 2
    OFFICE_ADMIN = 3
    ROLE_CHOICES = (
        (BHANTE, 'Bhante'),
        (SAYALAY, 'Sayalay'),
        (OFFICE_ADMIN, 'Office Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
