from django.contrib import admin

from .models import MyCustomuser, Payment, CorporateMemberRequest
# Register your models here.

admin.site.register([MyCustomuser, Payment, CorporateMemberRequest])