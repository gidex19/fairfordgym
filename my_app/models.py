from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

plan_type = (('1 Month','1 Month'), ('Quarterly','Quarterly'), ('6 Months','6 Months'), ('Yearly','Yearly'))
status_list  = (('Unpaid','Unpaid'), ('Pending','Pending'), ('Paid','Paid'), ('Active','Active'))

# Create your models here.
class MyCustomuser(AbstractUser):
    full_name = models.CharField(max_length=35, blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=60, blank=True)
    subscribed =  models.BooleanField(default=False)
    expiry_date = models.DateField(default=timezone.now)
    # user_category = models.CharField(max_length= 40, choices=user_types, default='Client')

    def __str__(self):
        return "User: {} \n email: {}".format(self.full_name, self.email)
    



class Payment(models.Model):
    user = models.ForeignKey(MyCustomuser, on_delete=models.CASCADE)
    # customers_name = models.CharField(max_length=70, blank=False)
    # customers_email = models.EmailField(max_length=100, blank=False)
    # customers_phone = models.CharField(max_length=11, blank=False)
    plan_type = models.CharField(max_length=100, choices=plan_type, blank=False)
    amount = models.PositiveIntegerField(default=0)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default='Unpaid', choices = status_list)
    reference = models.CharField(max_length=100, default='')
    date_created = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateField(default=timezone.now)