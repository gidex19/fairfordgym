from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

plan_type = (('1 Month','1 Month'), ('Quarterly','Quarterly'), ('6 Months','6 Months'), ('Yearly','Yearly'))
# hmo_list  = (('Prime Insurance','Prime Insurance'), ('XPC Corps','XPC Corps'), ('Axa Mansard','Axa Mansard'), ('Allen HMO','Allen HMO'))
hmo_list = ( ('No HMO Selected ', 'Select HMO'),('Axa Mansard', 'Axa Mansard'), ('Reliance', 'Reliance'), ('Avon', 'Avon'), ('Leadway', 'Leadway'), ('THT (Total health trust Ltd)', 'THT (Total health trust Ltd)'))
status_list  = (('Unpaid','Unpaid'), ('Pending','Pending'), ('Paid','Paid'), ('Active','Active'))
reason_list = (('Undefined', 'Undefined'), ('To Have Fun', 'To Have Fun'), ('To Keep Fit', 'To Keep Fit'), ('To Lose Weight', 'To Lose Weight'), ('To Meet New People', 'To Meet New People'), ('Recommended By Someone', 'Recommended By Someone'))



# Create your models here.
class MyCustomuser(AbstractUser):
    full_name = models.CharField(max_length=35, blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=60, blank=True, default='Undefined')
    subscribed =  models.BooleanField(default=False)
    expiry_date = models.DateField(default=timezone.now)
    is_corporate_user = models.BooleanField(default=False)
    profile_filled = models.BooleanField(default=False)

    date_of_birth = models.DateField(blank=True, null=True)
    reason = models.CharField(choices=reason_list, default='Undefined', max_length= 60)
    profile_pic = models.ImageField(default='default.jpg', blank=False)
    # user_category = models.CharField(max_length= 40, choices=user_types, default='Client')

    # def __str__(self):
    #     return "User: {} \n email: {}".format(self.full_name, self.email)
    

class CorporateMemberRequest(models.Model):
    full_name = models.CharField(max_length=35, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    hmo = models.CharField(max_length=100, choices=hmo_list, blank=False)
    company_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)
    treated = models.BooleanField(default=False)

    def __str__(self):
        status = ''
        if self.treated:
            status = "COMPELTED"
        else:
            status = "UNCOMPLEMENTED"    

        return "{} REQUEST: From {} of [{}] to {}".format(status,  self.full_name, self.company_name, self.hmo)

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
    used = models.BooleanField(default=False)

    def __str__(self):
        return "Payment by: {} \n email: {} on {}".format(self.user.full_name, self.user.email, self.date_created)
    
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=35, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}: Message from {} | {}".format(self.date_created, self.full_name, self.email)